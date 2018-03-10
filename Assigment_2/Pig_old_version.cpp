#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <sstream>
#include <utility>
using std::istringstream;
using std::cout;
using std::endl;
using std::vector;
using std::max;
using std::min;
using std::pair;

#define LIMIT 100

void calProbs (vector<vector<double>>& probs, int& target) {
	vector<double> pb (target+1, 0);
	pb[0] = 1;
	pb[1] = 0;
	for (int i = 2; i <= target; ++ i) {
		for (int j = 2; j <= min(i, 6); ++ j) {
			pb[i] += pb[i-j] / 6.0;
		}
	}
	
	for (int s = 2; s <= target; ++ s) {
		double tem = pb[s];
		probs[s][0] = pb[s];
		for (int i = 1; i < 6; ++ i) {
			for (int k = 2; k <= min(6, s+i); ++ k)
				if (k > i)
					probs[s][i] += pb[s+i-k] / 6.0;
			tem += probs[s][i];
		}
		probs[s][6] = 1 - tem;
	}
}

pair<double, int> piggame(int& target, int& player, int& rival) {
	vector<vector<vector<double>>> dp (target+1, vector<vector<double>>(target+1, vector<double>(2, 0.0)));
	vector<vector<double>> probs (target+1, vector<double> (7, 0.0));
	calProbs(probs, target);
	int r = 0, res = 0;
	while (r < LIMIT) {
		for (int i = player; i <= target; ++ i) { 
			for (int j = rival; j <= target; ++ j) {
				if (r == 0) {
					dp[i][j][r] = 0.5;
					continue;
				}
				if (i >= target) {
					dp[i][j][r%2] = 1.0;
					continue;
				}
				if (j >= target) {
					dp[i][j][r%2] = 0.0;
					continue;
				}
				if ((r%2) == 1) {
					double tem_res = 1;
					for (int s = 2; s <= max(2, target-j); ++ s) {
						double tem = dp[i][j][0] * probs[s][6];
						for (int k = s; k < s+6; ++ k)
							tem += dp[i][min(j+k, target)][0] * probs[s][k-s];
						tem_res = min(tem, tem_res);
					}	
					dp[i][j][1] = tem_res;
				}
				else {
					double tem_res = -1;
					for (int s = 2; s <= max(2, target-i); ++ s) {
						double tem = dp[i][j][1] * probs[s][6];
						for (int k = s; k < s+6; ++ k)
							tem += dp[min(i+k, target)][j][1] * probs[s][k-s];
						if (tem_res < tem) {
							tem_res = tem;
							if (i == player && j == rival) {
								res = s;
							}
						}
					}
					dp[i][j][0] = tem_res;
				}
			}
		}
		r ++;
	}
	return {dp[player][rival][0], res};
}

int main (int argc, char** argv) {
	if (argc > 3) {
		vector<int> parameters;
		for (int i = 1; i < 4; ++ i) {
			istringstream iss(argv[i]);
			int tem;
			iss >> tem;
			parameters.push_back(tem);
		}
		if (parameters[1] > parameters[0] || parameters[2] > parameters[0])
			return 0;
		auto res = piggame(parameters[0], parameters[1], parameters[2]);
		cout << res.first << " " << res.second << endl;
	}
	return 1;
}