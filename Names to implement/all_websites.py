import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_header(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        header1 = soup.find_all('h1')[1]  # Adjust the tag according to the main header on the websites
        header2 = soup.find('h2')  # Adjust the tag according to the main header on the websites
        return header1.text, header2
    except Exception as e:
        return url, None

def scrape_headers(urls):
    headers = []
    with ThreadPoolExecutor(max_workers=7) as executor:  # Adjust the number of workers as needed
        results = list(executor.map(get_header, urls))

    for result in results:
        header1, header2 = result
        if header1:
            headers.append(f"{header1}: {header2}")

    return headers

def save_to_txt(headers, output_file='output.txt'):
    with open(output_file, 'w') as file:
        for header in headers:
            file.write(header + '\n')

if __name__ == "__main__":
    # List of websites to scrape
    websites = [f"https://c9x.me/x86/html/file_module_x86_id_{id}.html" for id in range(1,333)]

    # Scrape headers in parallel
    headers = scrape_headers(websites)

    # Save headers to a text file
    save_to_txt(headers)

    print("Scraping complete. Headers saved to output.txt.")
