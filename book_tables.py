"""Display pandas Styler tables consistently in HTML and LaTeX output."""

from IPython.display import display


class _DualFormatStyler:
    """Expose both rich representations so Quarto can select the output format."""

    def __init__(self, styler):
        self.styler = styler

    def _repr_html_(self):
        return self.styler.to_html()

    def _repr_latex_(self):
        table = self.styler.to_latex(convert_css=True, hrules=True)
        return (
            "\\begin{adjustbox}{center,max width=\\linewidth}\n"
            f"{table}"
            "\\end{adjustbox}\n"
        )


def display_styled_table(styler):
    """Display a Styler with dynamic cell formatting in HTML and PDF."""

    display(_DualFormatStyler(styler))
