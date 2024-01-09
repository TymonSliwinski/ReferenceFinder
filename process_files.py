import argparse
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from pypdf import PdfReader

BACKNED_URL = os.environ.get('BACKNED_URL', 'http://localhost:5000')

def process_paragraph(paragraph, file_name, page_number, i):
    paragraph = paragraph.replace('-\n', '').replace('\n', ' ') + '.'
    response = requests.post(
        f'{BACKNED_URL}/api/embed',
        json={'text': paragraph},
        headers={'Content-Type': 'application/json'},
    )
    response.raise_for_status()

    vec_id = file_name + '_' + str(page_number) + '_' + str(i)
    values = response.json()
    metadata = {
        'file': file_name,
        'page': page_number,
        'text': paragraph,
    }

    return {
        'id': vec_id,
        'values': values,
        'metadata': metadata,
    }

def process_files(files_path: str):
    pdf_files = [
        os.path.join(files_path, file)
        for file in os.listdir(files_path)
        if os.path.isfile(os.path.join(files_path, file)) and file.endswith('.pdf')
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        for file in pdf_files:
            reader = PdfReader(file)
            file_name = os.path.basename(file)
            for page in reader.pages:
                vectors = []
                paragraphs = page.extract_text().split('.\n')
                page_number = page.page_number + 1
                futures = []

                for i, paragraph in enumerate(paragraphs, start=1):
                    future = executor.submit(process_paragraph, paragraph, file_name, page_number, i)
                    futures.append(future)

                for future in futures:
                    vector = future.result()
                    vectors.append(vector)

                if vectors:
                    response = requests.post(
                        f'{BACKNED_URL}/api/vectors/upload',
                        json={'vectors': vectors},
                        headers={'Content-Type': 'application/json'},
                    )
                    response.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description='Loads PDF files, embeds to vectors and uploads to backend')
    parser.add_argument('--path', type=str, help='Path to PDF files')
    args = parser.parse_args()

    if args.path:
        files_path = args.path

    process_files(files_path)

if __name__ == '__main__':
    main()
