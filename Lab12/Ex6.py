import requests
from bs4 import BeautifulSoup


URL = "https://www.hicentral.com/hawaii-mortgage-rates.php"


def fetch_page(url: str) -> str:
	"""Download page HTML and raise an error if request fails."""
	response = requests.get(
		url,
		timeout=20,
		headers={"User-Agent": "Mozilla/5.0 (MortgageRateScraper/1.0)"},
	)
	response.raise_for_status()
	return response.text


def extract_rate_rows(html: str):
	"""Find the mortgage rate rows and return normalized entries."""
	soup = BeautifulSoup(html, "html.parser")

	def looks_like_loan_type(text: str) -> bool:
		value = text.upper()
		return "FIXED" in value or "ARM" in value

	entries = []
	current_bank = ""

	for tr in soup.find_all("tr"):
		cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
		if not cells:
			continue

		# Rows generally look like:
		# [bank, loan_type, rate, points, apr] for first row of a bank
		# [loan_type, rate, points, apr] for subsequent rows
		if len(cells) >= 5 and not looks_like_loan_type(cells[0]):
			current_bank = cells[0]
			loan_type, rate, points, apr = cells[1], cells[2], cells[3], cells[4]
		elif len(cells) >= 4 and looks_like_loan_type(cells[0]) and current_bank:
			loan_type, rate, points, apr = cells[0], cells[1], cells[2], cells[3]
		else:
			continue

		entries.append(
			{
				"bank": current_bank,
				"loan_type": loan_type,
				"rate": rate,
				"points": points,
				"apr": apr,
			}
		)

	if not entries:
		raise ValueError("Could not find mortgage rate rows on the page.")

	return entries


def main():
	html = fetch_page(URL)
	rows = extract_rate_rows(html)

	print("Hawaii Mortgage Rates")
	print("-" * 60)

	for row in rows:
		print(
			f"{row['bank']} -> "
			f"{row['loan_type']} | Rate: {row['rate']} | "
			f"Points: {row['points']} | APR: {row['apr']}"
		)


if __name__ == "__main__":
	main()
