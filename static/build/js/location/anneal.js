var temperature = 0.1;
var ABSOLUTE_ZERO = 1e-4;
var COOLING_RATE = 0.999999;
var num_points = 50;
var current = [];
var best = [];
var best_cost = 0;

$(document).ready(function()
	{
		$("#solve").click(function()
			{
				temperature = parseFloat($("#temperature").val());
				ABSOLUTE_ZERO = parseFloat($("#abszero").val());
				COOLING_RATE = parseFloat($("#coolrate").val());
				num_points = parseInt($("#cities").val());
				init_graph();
			});
	});

function randomFloat(n)
{
	return (Math.random()*n);
}

function randomInt(n)
{
	return Math.floor(Math.random()*(n));
}

function randomInteger(a,b)
{
	return Math.floor(Math.random()*(b-a)+a);
}

function deep_copy(array, to)
{
	var i = array.length;
	while(i--)
	{
		to[i] = [array[i][0],array[i][1]];
	}
}

function getCost(route)
{
	var cost = 0;
	for(var i=0; i< num_points-1; i++)
	{
		cost = cost + getDistance(route[i], route[i+1]);
	}
	cost = cost + getDistance(route[0],route[num_points-1]);
	return cost;
}

function getDistance(p1, p2)
{
    console.log(p1[0], p1[1]);
	var del_x = (p1[0] - p2[0]) * 1000;
	var del_y = (p1[1] - p2[1]) * 1000;
	return Math.sqrt((del_x*del_x) + (del_y*del_y));
}

function mutate2Opt(route, i, j)
{
	var neighbor = [];
	deep_copy(route, neighbor);
	while(i != j)
	{
		var t = neighbor[j];
		neighbor[j] = neighbor[i];
		neighbor[i] = t;

		i = (i+1) % num_points;
		if (i == j)
			break;
		j = (j-1+num_points) % num_points;
	}
	return neighbor;
}

function acceptanceProbability(current_cost, neighbor_cost)
{
	if(neighbor_cost < current_cost)
		return 1;
	return Math.exp((current_cost - neighbor_cost)/temperature);
}

//10 => 0.99
//100 => 0.9999
//f(x) = 1 - 1/x*x

function init_graph(points)
{
	//for(var i=0; i<num_points; i++)
	//{
	//	current[i] = [randomInteger(10,tsp_canvas.width-10),randomInteger(10,tsp_canvas.height-10)];
	//}
    current = points;
	num_points = points.length;
    COOLING_RATE = 1 - 1 / num_points * num_points;

    temperature = 0.1

	deep_copy(current, best);
	best_cost = getCost(best);
	//setInterval(solve, 10);
	while (temperature>ABSOLUTE_ZERO) {
		solve()
	}
	return best;
}

function solve()
{
	var current_cost = getCost(current);
	var k = randomInt(num_points);
	var l = (k+1+ randomInt(num_points - 2)) % num_points;
	if(k > l)
	{
		var tmp = k;
		k = l;
		l = tmp;
	}
	var neighbor = mutate2Opt(current, k, l);
	var neighbor_cost = getCost(neighbor);
	if(Math.random() < acceptanceProbability(current_cost, neighbor_cost))
	{
		deep_copy(neighbor, current);
		current_cost = getCost(current);
	}
	if(current_cost < best_cost)
	{
		deep_copy(current, best);
		best_cost = current_cost;
		//paint();
	}
	temperature *= COOLING_RATE;
}
