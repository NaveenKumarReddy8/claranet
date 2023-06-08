"""Calculate the sum of all elements in a submatrix in constant time.

Given an M × N integer matrix and two coordinates (p, q) and (r, s) representing top-left and bottom-right coordinates of a submatrix of it,
calculate the sum of all elements present in the submatrix. Here, 0 <= p < r < M and 0 <= q < s < N.
"""

from logging import DEBUG, FileHandler, Formatter, Logger, getLogger
from sys import exit

# logger setup.
logger: Logger = getLogger("claranet-dsa")
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = FileHandler(filename="dsa_logs.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(level=DEBUG)
logger.addHandler(file_handler)
logger.setLevel(level=DEBUG)


class SumOfSubMatrix:
    """Class for calculating the sum of sub-matrix."""

    def __init__(self, matrix: list[list[int]]) -> None:
        """Initializer for the class.

        Args:
            matrix (list[list[int]]): Input matrix.
        """
        self.matrix: list[list[int]] = matrix

    def get_sum_of_sub_matrix(self, p: tuple[int, int], q: tuple[int, int]) -> int:
        """Calculates the sum of all elements in the sub-matrix.

        Args:
            p (tuple[int, int]): x and y coordinates of the point P.
            q (tuple[int, int]): x and y coordinates of the point Q.

        Returns:
            int: sum of all elements in the sub-matrix.

        """
        return sum([sum(row[p[1] : q[1] + 1]) for row in self.matrix[p[0] : q[0] + 1]])


def get_matrix_size() -> tuple[int, int]:
    """Fetches the size of the matrix as input from the user.

    Returns:
        tuple[int, int]: Number of rows and columns of the matrix.

    """
    try:
        rows, columns = input("Please enter the size of the matrix rows and columns separated by space:\t").split()
        logger.info(f"matrix size is: {rows}x{columns}")
        return int(rows), int(columns)
    except ValueError as exc:
        logger.error(f"ValueError: {exc}")
        print("Please enter only 2 integers as input.")
        exit(1)


def get_matrix(rows: int, columns: int) -> list[list[int]]:
    """Fetches the matrix as input from the user.

    Args:
        rows (int): Number of rows.
        columns (int): Number of columns.

    Returns:
        list[list[int]]: Matrix fetched from the user.

    """
    print("Please enter the values separated by space for each row prompt:")
    matrix: list[list[int]] = []
    for row in range(rows):
        try:
            row_data = list(map(int, input(f"row {row}:\t").split()))
            if len(row_data) != columns:
                logger.error(f"Length of row_data: {row_data} is not equal to columns: {columns}")
                raise ValueError(f"Please enter {columns} number of values.")
            matrix.append(row_data)
        except ValueError as exc:
            logger.error(f"ValueError: {exc}")
            print(f"ValueError: {exc}")
            exit(1)
    logger.debug(f"The matrix is: {matrix}")
    return matrix


def display_matrix(matrix: list[list[int]]) -> None:
    """Prints the matrix on the console.

    Args:
        matrix (list[list[int]]): Matrix input from the user.

    Returns:
        None: NoneType object.

    """
    print("The input matrix is:")
    for row in matrix:
        print(*row, sep="\t")


if __name__ == "__main__":
    # input.
    x, y = get_matrix_size()
    matrix = get_matrix(rows=x, columns=y)
    display_matrix(matrix=matrix)

    # sum of sub matrix.
    sum_of_sub_matrix = SumOfSubMatrix(matrix=matrix)
    while True:
        try:
            p_x, p_y = map(
                int,
                input("Please enter the x and y coordinates of point P separated by space:\t").split(),
            )
            q_x, q_y = map(
                int,
                input("Please enter the x and y coordinates of point Q separated by space:\t").split(),
            )
            if (p_x >= x) or (p_y >= y) or (q_x >= x) or (q_y >= y):
                raise ValueError(f"Please enter x values in between 0 and {x-1} and y values in between 0 and {y-1}")
            answer: int = sum_of_sub_matrix.get_sum_of_sub_matrix(p=(p_x, p_y), q=(q_x, q_y))
            print("*" * 60)
            print(f"The sum of the sub-matrix is {answer}. Please enter ctrl+c to quit.")
            print("*" * 60)
        except ValueError as exc:
            logger.error(f"ValueError: {exc}")
            print(f"ValueError: Invalid Input: {exc}")
        except KeyboardInterrupt:
            print("Thank you")
            logger.debug("Program executed successfully.")
            exit(0)
