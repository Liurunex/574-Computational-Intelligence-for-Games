#include <string>
#include <cstring>
#include <iostream>
#include <unordered_set>
#include <vector>
#include <algorithm>
#include <climits>
#include <sstream>
using std::istringstream;
using std::unordered_set;
using std::strcmp;
using std::string;
using std::cout;
using std::endl;
using std::vector;
using std::max;

int findMex (unordered_set<int>& nimbers) {
	int mex = 0;
	while (nimbers.count(mex))
		mex ++;
	return mex;
}

int find_Grundy(int n, vector<int>& grundy_arr) {
	if (n > 0) grundy_arr[1] = 1;
	if (n > 1) grundy_arr[2] = 0;
	if (grundy_arr[n] != -1)
		return grundy_arr[n];

	unordered_set<int> nimbers;
	for (int i = 0; i < n-1; ++ i) {
		nimbers.insert(find_Grundy(i, grundy_arr)^find_Grundy(n-i-2, grundy_arr));
	}
	grundy_arr[n] = findMex(nimbers);
	return grundy_arr[n];
}

string find_Way(string& board, vector<int>& sub_game, vector<int>& grundy_arr, vector<int>& sub_indexs) {
	string res = board;
	vector<string> solutions;
	vector<int> sol_size;
	int sn = sub_game.size();
	for (int i = 0; i < sn; ++ i) {
		int grundy = 0;
		if (sub_game[i] == 1) {
			for (int j = 0; j < sn; ++ j) {
				if (i != j)
					grundy ^= grundy_arr[sub_game[j]];
			}
			if (!grundy) {
				res[sub_indexs[i]] = '.';
				solutions.push_back(res);
				sol_size.push_back(sn-1);
				res = board;
			}
		}
		else if (sub_game[i] == 2)
			continue;
		else {
			for (int k = 0; k < sub_game[i]-1; ++ k) {
				grundy = grundy_arr[k]^grundy_arr[sub_game[i]-k-2];
				for (int j = 0; j < sn; ++ j) {
					if (i != j)
						grundy ^= grundy_arr[sub_game[j]];
				}
				if (!grundy) {
					res[sub_indexs[i]+k] = '.';
					res[sub_indexs[i]+k+1] = '.';
					solutions.push_back(res);
					
					int thesize = sn-1;
					if (k > 0) thesize ++;
					if (sub_game[i]-k-2 > 0) thesize ++;
					sol_size.push_back(thesize);
					
					res = board;
				}
			}
		}
	}
	int sol_min = INT_MAX, tar_index = -1;
	for (int i = 0; i < (int)sol_size.size(); ++ i) {
		if (sol_size[i] < sol_min) {
			sol_min = sol_size[i];
			tar_index = i;
		}
	}
	return solutions[tar_index];
}

int main (int argc, char** argv) {
	if (argc > 2 && !strcmp(argv[1], "grundy")) {
		int n = 0;
		istringstream iss(argv[2]);
		iss >> n;

		vector<int> grundy_arr (n+1, -1);
		grundy_arr[0] = 0;
		
		for (int i = 1; i <= n ; ++ i)
			find_Grundy(i, grundy_arr);

		cout << "[";
		for (int i = 0; i < n+1; ++ i) {
			if (i != 0) cout << " ";
			cout << grundy_arr[i];
			if (i != n) cout << ",";
		}
		cout << "]" << endl;
	}
	else {
		if (argc < 2) {
			cout << "LOSS" << endl;
			return 1;
		}
		string board(argv[1]);
		if (board.find_first_not_of(".x") != string::npos)
			return 1;
		int count = 0, index = 0, max_game = 0, n = board.size();
		while (index < n && board[index] == '.')
			index ++;
		if (index >= n) {
			cout << "LOSS" << endl;
			return 1;
		}
		vector<int> sub_game, sub_indexs;
		sub_indexs.push_back(index);
		for (int i = index; i < n; ++ i) {
			if (board[i] == 'x')
				count ++;
			else {
				sub_game.push_back(count);
				max_game = max(max_game, count);
				count = 0;
				while (i < n && board[i] == '.')
					i ++;
				if (i < n)
					sub_indexs.push_back(i --);
			}
		}
		if (count) {
			sub_game.push_back(count);
			max_game = max(max_game, count);
		}
		vector<int> grundy_arr (max_game+1, -1);
		grundy_arr[0] = 0;
		for (int i = 1; i <= max_game; ++ i)
			find_Grundy(i, grundy_arr);
		int res = grundy_arr[sub_game[0]];
		for (int i = 1; i < (int)sub_game.size(); ++ i)
			res ^= grundy_arr[sub_game[i]];
		
		if (!res)
			cout << "LOSS" << endl;
		else {
			string uboard = find_Way(board, sub_game, grundy_arr, sub_indexs);
			cout << uboard << endl;
		}
	}
	return 1;
}