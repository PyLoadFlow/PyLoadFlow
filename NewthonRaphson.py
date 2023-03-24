import attrs
install_extras(["numpy", "attrs"])  # type: ignore

@attrs.define
class NewtonRaphson:
    F: list[function]
    X: list[float]