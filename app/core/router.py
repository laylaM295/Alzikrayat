
import re


class Router:
    """
    Custom manual router that matches URLs using regular expressions
    and dispatches requests to the appropriate controller method.
    """

    def __init__(self):
        """
        Initialize the router with an empty list of routes.
        """

        self.routes = []

    def add(self, method, routePath, controller):
        """
        Add a new route to the router.

        Args:
            method (str): HTTP method such as GET or POST.
            routePath (str): URL pattern such as /photo/{id}.
            controller:
                A tuple containing a controller instance and
                method name, or a callable function.
        """

        pattern = re.sub(
            r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}",
            r"([^/]+)",
            routePath
        )

        pattern = "^" + pattern + "$"

        self.routes.append({
            "method": method.upper(),
            "pattern": re.compile(pattern),
            "controller": controller
        })

    def dispatch(self, method, path):
        """
        Find a matching route and execute its controller method.

        Args:
            method (str): HTTP method of the request.
            path (str): Requested URL path.

        Returns:
            Any: Result returned by the controller method.

        Raises:
            ValueError: If no matching route is found.
        """

        method = method.upper()

        for route in self.routes:

            if route["method"] != method:
                continue

            match = route["pattern"].match(path)

            if not match:
                continue

            controller = route["controller"]

            parameters = match.groups()

            if isinstance(controller, tuple):

                controllerObject, methodName = controller

                controllerMethod = getattr(
                    controllerObject,
                    methodName
                )

                return controllerMethod(
                    *parameters
                )

            if callable(controller):

                return controller(
                    *parameters
                )

        raise ValueError("Route not found")
