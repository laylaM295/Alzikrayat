
from flask import render_template


class BaseController:
    """
    Base controller that provides common functionality
    for all application controllers.
    """

    def render(self, view, data=None):
        """
        Render a template with the provided data.

        Args:
            view (str): Name of the view template.
            data (dict): Data passed to the template.

        Returns:
            Response: Rendered Flask response.
        """

        return render_template(
            view + ".html",
            **(data or {})
        )