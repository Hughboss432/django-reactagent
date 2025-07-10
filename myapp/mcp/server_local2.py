from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP(name="localserver")

@mcp.tool()
def bisection_method(a: float, b: float, max_iter: int, precision: int, func_str: str) -> str:
    """
    Estimate the root of a function using the **Bisection Method**.

    Use this when:
    - The function is continuous and changes sign over [a, b].
    - A safe and guaranteed method is preferred, even if slower.

    Parameters:
    - a, b: Interval boundaries.
    - max_iter: Max number of iterations.
    - precision: Decimal accuracy (e.g. 4 means 10^-4).
    - func_str: Function as string using variable 'x' (e.g., 'x**2 - 4').

    Returns:
    - Estimated root and absolute error.
    """
    x = a
    iter_count = 0
    Er = 1
    while Er >= 10**(-precision) and iter_count < max_iter:
        x_old = x
        x_new = (a + b) / 2
        iter_count += 1
        Er = abs(x_new - x_old)

        x = x_new
        fx = eval(func_str)
        x = a
        fa = eval(func_str)

        if fa * fx < 0:
            b = x_new
        else:
            a = x_new

    return f"Final result after {iter_count} iterations: x ≈ {x_new} with absolute error ≈ {Er}"

@mcp.tool()
def false_position(a: float, b: float, max_iter: int, precision: int, func_str: str) -> str:
    """
    Estimate the root using the **False Position Method** (Regula Falsi).

    Use this when:
    - Function is continuous and changes sign over [a, b].
    - You want a slightly faster method than bisection.

    Parameters:
    - a, b: Interval endpoints.
    - max_iter: Max iterations.
    - precision: Desired accuracy.
    - func_str: Function as a string (e.g. 'x**3 - x').

    Returns:
    - Estimated root and absolute error.
    """
    fa = eval(func_str.replace("x", str(a)))
    fb = eval(func_str.replace("x", str(b)))

    if fa * fb > 0:
        return "Function does not change sign over the interval. Try a different [a, b]."

    x_old = a
    iter_count = 0
    Er = 1

    while Er >= 10**(-precision) and iter_count < max_iter:
        x = b - fb * (b - a) / (fb - fa)
        iter_count += 1
        fx = eval(func_str.replace("x", str(x)))

        Er = abs(x - x_old)
        x_old = x

        if fa * fx < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    return f"Final result after {iter_count} iterations: x ≈ {x} with absolute error ≈ {Er}"

@mcp.tool()
def newton_method(x: float, precision: int, max_iter: int, func_str: str, deriv_str: str) -> str:
    """
    Estimate the root using the **Newton-Raphson Method**.

    Use this when:
    - You have both the function and its derivative.
    - Fast convergence is desired and derivative is non-zero.

    Parameters:
    - x: Initial guess.
    - precision: Decimal precision (e.g. 5 for 10^-5).
    - max_iter: Max iterations.
    - func_str: Function as a string (e.g. 'x**2 - 2').
    - deriv_str: Derivative as a string (e.g. '2*x').

    Returns:
    - Estimated root and relative error.
    """
    iter = 0
    er = 1
    while er >= 10**(-precision) and iter < max_iter:
        x_old = x
        fx = eval(func_str)
        dfx = eval(deriv_str)

        if dfx == 0:
            return "Zero derivative. Method failed."

        x = x_old - fx / dfx
        er = abs((x - x_old) / x)
        iter += 1

    return f"Final result after {iter} iterations: x ≈ {x} with relative error ≈ {er}"

@mcp.tool()
def secant_method(x0: float, x1: float, precision: int, max_iter: int, func_str: str) -> str:
    """
    Estimate the root using the **Secant Method**.

    Use this when:
    - You don't have the derivative.
    - You want faster convergence than bisection.

    Parameters:
    - x0, x1: Two initial guesses.
    - precision: Desired accuracy (decimal digits).
    - max_iter: Max number of iterations.
    - func_str: Function as string (e.g. 'x**2 - 3').

    Returns:
    - Estimated root and relative error.
    """
    iter = 0
    er = 1

    while er >= 10**(-precision) and iter < max_iter:
        x = x0
        f_x0 = eval(func_str)
        x = x1
        f_x1 = eval(func_str)

        if (f_x1 - f_x0) == 0:
            return "Division by zero. Method failed."

        x2 = x1 - f_x1 * (x0 - x1) / (f_x0 - f_x1)
        er = abs((x2 - x1) / x2)

        x0 = x1
        x1 = x2
        iter += 1

    return f"Final result after {iter} iterations: x ≈ {x2} with relative error ≈ {er}"

# run server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")