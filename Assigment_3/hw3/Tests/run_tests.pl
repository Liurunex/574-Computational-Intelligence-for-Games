&sectionHeader('Payoff Matrix (Optional)');
@SOURCE = ();
@LINK = ('/c/cs474/hw3/Tests/plays.py', '/c/cs474/hw3/Tests/two_minute.pickle', '/c/cs474/hw3/Tests/two_minute.csv');
$subtotal = &runTest('001', 'Start of game');
$subtotal += &runTest('002', 'Midfield');
$subtotal += &runTest('003', 'Goal to Go');
$subtotal = $subtotal * 0 / 3;
$total += floor($subtotal);
&sectionResults('Payoff Matrix (Optional)', $subtotal);

&sectionHeader('Full Output');
@SOURCE = ();
@LINK = ('/c/cs474/hw3/Tests/plays.py', '/c/cs474/hw3/Tests/two_minute.pickle', '/c/cs474/hw3/Tests/two_minute.csv');
$subtotal = &runTest('004', 'Start of game');
$subtotal += &runTest('005', 'Midfield');
$subtotal += &runTest('006', 'Goal to Go');
$total += floor($subtotal);
&sectionResults('Full Output', $subtotal);

