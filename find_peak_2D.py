def find_peak_2D(A, r = None, w = None):
	'''
	Find a peak in a two dimensional array.
	Input: 2D integer array A, subarray indices r, witness w
	'''
	if r is None:
		r = (0, 0, len(A[0]) - 1, len(A) - 1)
	px, py, qx, qy = r  # A[py][px] upper left, A[qy][qx] lower right
	if w is None:
		w = (0, 0)
	wx, wy = w          # A[wy][wx] witness
	# wx = (px + qx)//2
	for i in range(py, qy):
		if A[wy][wx] < A[i][wx]:
			wy = i

	if A[wy][wx - 1] > A[wy][wx]:
		find_peak_2D(A, (px, py, wx - 1, qy), ((px + wx - 1)//2, wy))
	elif A[wy][wx + 1] > A[wy][wx]:
		find_peak_2D(A, (wx + 1, py, qx, qy), ((wx + 1 + qx)//2, wy))

	return wx, wy


