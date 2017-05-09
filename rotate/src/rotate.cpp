#include <iostream>
#include <vector> 
#include <math.h> 

using namespace std; 

int main () {

	int elem, n;
	vector<int> matrix;

	while (cin >> elem) {
		matrix.push_back(elem);
	} 
	
	n = floor(sqrt(matrix.size()));

		for (int j = 0; j < n; ++j) {
		for (int i = n - 1; i >= 0; --i) {
			cout << matrix[i * n + j] << " "; 
		}
		cout << endl;
	}

	return 0;
}