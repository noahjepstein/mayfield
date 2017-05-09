#include <iostream>
#include <fstream>
#include <vector> 
#include <math.h> 

using namespace std; 

int main (int argc, char* argv[]) {

	int elem, n;
	vector<int> matrix;
	ifstream input_file;

	if (argc > 0) {
		input_file.open(argv[1]);
	} else {
		cout << "Please specify a filename for rotating." << endl;
		cout << "Usage: ./rotate my_NxN_int_array.txt" << endl;
		exit(1);
	}

	while (input_file.is_open() && !input_file.eof()) {
		input_file >> elem;
		matrix.push_back(elem);
	} 
	input_file.close();
	n = floor(sqrt(matrix.size()));

	/* Would be faster to store array as column major __if__ we were 
	   traversing the array more than once. However, since the read
	   will be faster for row major access, and we only do one read 
	   and one write, the choice doesn't matter... 
	 */
	for (int j = 0; j < n; ++j) {
		for (int i = n - 1; i >= 0; --i) {
			cout << matrix[i * n + j] << " "; 
		}
		cout << endl;
	}

	return 0;
}