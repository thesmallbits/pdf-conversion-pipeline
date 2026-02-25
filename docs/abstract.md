# Creating a pipeline to convert pdfs into structured json

The simplified workflow for converting pdfs into structured json is

## Step 0: Infrastructure

The infrastructure consists of two Docker containers, one for the FastAPI server hosting the python API for external communication, and another for running a Mistral instance on ollama

## Step 1: PDF upload

1. A post request is sent to the (/upload) endpoint of FastAPI container
2. The pdf is split into pages, and each page is converted indivisually into Markdown and its constituent images
    1. The PDF is split so as to reduce the ram used by the Marker's conversion pipeline
    2. The default Marker's JSONRenderer generates alot of noise like inline html and irrelevent content, which would require further parsing logic. Rather we'll just convert the PDF to markdown and pipe that to the Ollama instance to extract questions and the relevant options

## Step 2: Marker conversion pipeline

1. The PDF -> Markdown conversion is done with the help of [Marker](https://github.com/datalab-to/marker) and it runs on the GPU.
    - It _could_ be run on CPU as well, but it took nearly 10 minutes to convert a single page
    - The gpu based pipeline is working fine on CUDA Version 12.8 with 570.211 (ig proprietery ones ??) NVIDIA drivers.
    - The whole process takes about 5gigs of VRAM (out of my 6gigs, so it might take more if the hardware allows)
2. Indivisual pages are converted to markdown and are saved to a tmp folder along with their respective base64 encoded strings

Post conversion content.

```
outputs/markdowns
├── bar.pdf_UYurk2uayI
│   ├── metadata.json
│   ├── page_1_content.json
│   ├── page_1_images.json
│   ├── page_2_content.json
│   └── page_2_images.json
└── foo.pdf_q8fJ1kyFu3
    ├── metadata.json
    ├── page_1_content.md
    ├── page_1_images.md
    ├── page_2_content.md
    ├── page_2_images.md
    ├── page_3_content.md
    └── page_3_images.md

3 directories, 10 files
```

- `metadata.json` contains properties about the converted pdf like
    - Name of pdf
    - Total images
    - Timestamp of pdf conversion (because why not)

## Step 3: Markdown cleaning and question extraction

1. Each markdown page would be fed into the Ollama instance OR if aukad provides, into an external LLM API
    - The ollama (mistral) instance is kinda slow taking about

    ```
    [GIN] 2026/02/25 - 10:34:47 | 200 |  1.367179065s |      172.21.0.1 | POST     "/api/chat"      // Was simple 'hi'
    [GIN] 2026/02/25 - 10:35:05 | 200 |  6.960025618s |      172.21.0.1 | POST     "/api/chat"      // IDK was smth
    [GIN] 2026/02/25 - 10:35:13 | 200 |   1.12924516s |      172.21.0.1 | POST     "/api/chat"
    [GIN] 2026/02/25 - 10:35:47 | 200 | 15.855479216s |      172.21.0.1 | POST     "/api/chat"
    [GIN] 2026/02/25 - 10:36:25 | 200 |  5.675426199s |      172.21.0.1 | POST     "/api/chat"
    [GIN] 2026/02/25 - 10:41:41 | 200 |         2m22s |      172.21.0.1 | POST     "/api/chat"      // Debugging question
    ```

    So maybe also write a benchmark to test various LLMs

2. THe prompt given to the LLM could be something like

```
you are <something something>, from this raw markdown text extract all the questions as is along with their corresponding options (if present) and return a corresponding JSON object from it


<we'd give some standard examples for it to work with>

# RULES AND EXAMPLES


0. The response should be an array of objects with the following schema <work on it>
    ~~~
    {
        question_number: number,
        question_type: "multiple-choice" | "theoriotical" | "assertion-reason" <add more patterns here>
        question_text: string,
        question_options: null (IF THE QUESTION IS QUESTION ANSWER OR REASONING BASED) or else array of objects {option_label: string, option_content: string}
        question_image: name of the image tag which is most nearby to the question in the source markdown
    }
    ~~~

1. Preserve all the text of both the questions and options as it is, including any inline formatting, LATEX equations / syntax
2. If any image is found, append its "source name" to the MOST APPROPRIATE OR NEARBY QUESTION.
3. Skip / Ignore any filler text such as Headers, Titles, Watermarks etc <or maybe we could append it along with the generated json idk>

Some conversion examples include
<pl give examples im chink>
```

3. Each json is saved in separate folder such as

```
outputs/json
├── bar.pdf_UYurk2uayI
│   ├── metadata.json
│   ├── page_1_content.json
│   ├── page_1_images.json
│   ├── page_2_content.json
│   └── page_2_images.json
└── foo.pdf_q8fJ1kyFu3
    ├── metadata.json
    ├── page_1_content.json
    ├── page_1_images.json
    ├── page_2_content.json
    ├── page_2_images.json
    ├── page_3_content.json
    └── page_3_images.json
```

3. Compilation of transformed

ALl JSON objects are combined into a single json array along with a separate map of image names to their base64 encoded strings

> [!NOTE] since we gonna process each page indivisually, it is possible that the image names clash if Marker generates them as _image_1.png_, _image_2.png_ and so on

## Step 4: JSON Response

The compiled Question, Option and Image json along with some metadata (like creation datetime, random uuid etc) is sent back as response

---

## Notes

- The `text_from_rendered` function takes the Render Object returned by the `PdfConverter` and it always returns values
    1. Plaintext string for all Markdown, HTML as well as JSON (json also gets returned as string)
    2. Type of first value `"json" | "json" | "html`
    3. Image dict with keys as image name and values as Pillow image objects

- Change the processing device by changing as

```py
converter = PdfConverer(
    artifact_dict=create_model_dict(
        device = "cuda"
        # OR
        device = "cpu"
    ),
)
```

- Output Renderer can be changed by passing the class path of target output in the `renderer` argument while constructing the `PdfConverer` object

```py
converter = PdfConverer(
    artifact_dict=create_model_dict(),
    rendrer="marker.renderers.json.JSONRenderer" # use the json renderer
)
converter = PdfConverer(
    artifact_dict=create_model_dict(),
    rendrer="marker.renderers.html.HTMLRenderer" # use the json renderer
)
```

- `config` opts taken by the PDFRenderer

```
    page_range: Annotated[
        List[int],
        "The range of pages to process.",
        "Default is None, which will process all pages.",
    ] = None
    pdftext_workers: Annotated[
        int,
        "The number of workers to use for pdftext.",
    ] = 4
    flatten_pdf: Annotated[
        bool,
        "Whether to flatten the PDF structure.",
    ] = True
    force_ocr: Annotated[
        bool,
        "Whether to force OCR on the whole document.",
    ] = False
    ocr_invalid_chars: Annotated[
        tuple,
        "The characters to consider invalid for OCR.",
    ] = (chr(0xFFFD), "�")
    ocr_space_threshold: Annotated[
        float,
        "The minimum ratio of spaces to non-spaces to detect bad text.",
    ] = 0.7
    ocr_newline_threshold: Annotated[
        float,
        "The minimum ratio of newlines to non-newlines to detect bad text.",
    ] = 0.6
    ocr_alphanum_threshold: Annotated[
        float,
        "The minimum ratio of alphanumeric characters to non-alphanumeric characters to consider an alphanumeric character.",
    ] = 0.3
    image_threshold: Annotated[
        float,
        "The minimum coverage ratio of the image to the page to consider skipping the page.",
    ] = 0.65
    strip_existing_ocr: Annotated[
        bool,
        "Whether to strip existing OCR text from the PDF.",
    ] = False
    disable_links: Annotated[
        bool,
        "Whether to disable links.",
    ] = False
    keep_chars: Annotated[
        bool,
        "Whether to keep character-level information in the output.",
    ] = False
```
