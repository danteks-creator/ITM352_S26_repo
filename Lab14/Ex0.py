"""Check whether selected third-party packages are installed."""

from importlib.util import find_spec


def check_package(package_name: str) -> bool:
	"""Return True if package can be found in current Python environment."""
	return find_spec(package_name) is not None


def main() -> None:
	packages = ["scipy", "statsmodels", "matplotlib"]
	print("Package installation report:")
	for name in packages:
		status = "INSTALLED" if check_package(name) else "NOT INSTALLED"
		print(f"- {name}: {status}")


if __name__ == "__main__":
	main()
