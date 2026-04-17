import numpy as np

def calculate_optimal_rotation(coords: np.ndarray, max_atoms: int = 2000) -> np.ndarray | None:
    """
    Calculates the optimal 3x3 rotation matrix using PCA to align the molecule
    so that its principal axes of variance correspond to the screen X, Y axes.
    Returns None if the number of atoms exceeds max_atoms, to avoid performance limits.
    """
    if len(coords) < 3 or len(coords) > max_atoms:
        return None

    # Center the coordinates
    centroid = np.mean(coords, axis=0)
    centered = coords - centroid

    # Calculate covariance matrix
    # coords shape is (N, 3), rowvar=False means columns are variables
    cov = np.cov(centered, rowvar=False)

    # Calculate eigenvectors and eigenvalues
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Sort by eigenvalues descending
    idx = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, idx]

    # The eigenvectors form our new basis U.
    # We want to rotate the data such that x_new = U.T * x_old
    # So our rotation matrix R = U.T
    R = sorted_eigenvectors.T

    # Ensure it's a proper rotation matrix (det(R) == 1, no reflection)
    if np.linalg.det(R) < 0:
        # Flip the 3rd row (which corresponds to the Z-axis / smallest principal component)
        R[2, :] *= -1

    return R.astype(np.float32)

def align_molecule_widget(widget, max_atoms: int = 2000) -> None:
    """
    Aligns the atoms inside a fastmolwidget MoleculeWidget automatically
    using PCA rotation. Evaluates widget._coords_array.
    """
    try:
        if not widget.atoms or len(widget.atoms) < 3:
            return

        # Get coordinates via the widget's internal array
        coords = widget._coords_array

        R = calculate_optimal_rotation(coords, max_atoms=max_atoms)
        if R is None:
            return

        # Track the cumulative rotation matrix
        widget.cumulative_R = np.dot(R, widget.cumulative_R)

        # Single bulk vector rotation
        widget._coords_array = np.dot(widget._coords_array - widget.molecule_center, R.T) + widget.molecule_center

        if np.any(widget._has_adp):
            widget._ucart_array = np.matmul(R, np.matmul(widget._ucart_array, R.T))
            widget._eigenvectors_array = np.matmul(R, widget._eigenvectors_array)
            widget._u_inv_array = np.matmul(R, np.matmul(widget._u_inv_array, R.T))

        for i, at in enumerate(widget.atoms):
            at.coordinate = widget._coords_array[i]
            at.z = at.coordinate[2]  # cache explicit z property for fast sorting
            if widget._has_adp[i]:
                at.u_cart = widget._ucart_array[i]
                at.u_eigvecs = widget._eigenvectors_array[i]
                at.u_inv = widget._u_inv_array[i]

        widget.repaint()
    except Exception as e:
        print(f"Exception during molecule auto-alignment: {e}")
