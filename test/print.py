# import subprocess
# import os

# def print_pdf(pdf_path):
#     """Prints a PDF file using the system's default printer.

#     Args:
#         pdf_path: The path to the PDF file.
#     """

#     if not os.path.exists(pdf_path):
#         raise FileNotFoundError(f"PDF file not found: {pdf_path}")

#     if os.name == 'nt':  # Windows
#         # Adjust the printer name if needed.  Use a command like "wmic printer list brief" to find available printers
#         command = ["cmd", "/c", "start", "", "AcroRd32", "/t", pdf_path] #Acrobat Reader
#         #Alternative for other PDF viewers (like Foxit Reader):
#         #command = ["cmd", "/c", "start", "", "FoxitReader.exe", pdf_path]
#     elif os.name == 'posix':  # Linux, macOS, BSD...
#         # 'lp' is the common command, but it might be different on some systems.  Use 'lp -d <printer_name> <file>' to specify printer
#         command = ["lp", pdf_path]  #Try with "lp -d <printer_name> <pdf_path>" to specify the printer
#     else:
#         raise OSError("Unsupported operating system.")

#     try:
#         subprocess.run(command, check=True, shell=False) # shell=False is important for security
#         print(f"Printing {pdf_path}...")
#     except subprocess.CalledProcessError as e:
#         print(f"Error printing PDF: {e}")
#     except FileNotFoundError as e:
#         print(f"Error: PDF reader not found.  Make sure it is in your system PATH.")


# # Example usage:
# pdf_file_path = "./ex/sefaresh_1599.pdf"  # Replace with your PDF file path
# print_pdf(pdf_file_path)

import aspose.pdf as ap

# Create PdfViewer object
viewer = ap.facades.PdfViewer()

# Open input PDF file
viewer.bind_pdf("./ex/sefaresh_1599.pdf")

# Print a PDF document
viewer.print_document()

# Close PDF file
viewer.close()