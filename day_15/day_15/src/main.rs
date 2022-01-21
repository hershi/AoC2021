use std::collections::BinaryHeap;
use std::cmp::Ordering;
use std::collections::HashSet;
use std::collections::HashMap;
use std::io::prelude::*;
use std::iter;
use std::io::BufReader;
use std::fs::File;

#[derive(Eq, PartialEq,Debug, Clone)]
struct HeapItem {
    pos: (usize, usize),
    dist: usize,
    prev: Option<(usize, usize)>,
}

impl Ord for HeapItem {
    fn cmp(&self, other: &Self) -> Ordering {
        other.dist.cmp(&self.dist)
    }
}

impl PartialOrd for HeapItem {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

struct Grid {
    grid: Vec<u8>,
    width: usize,
    height: usize,
}

impl Grid {
    fn new(grid: Vec<u8>, width :usize, height :usize) -> Grid {
        Grid{grid, width, height}
    }

    fn get(&self, x : usize, y : usize) -> usize {
        return self.grid[y * self.width + x] as usize
    }

    fn neighbors(&self, x :usize, y :usize) -> Vec<(usize,usize)> {
        let x = x as isize;
        let y = y as isize;
        vec![(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            .iter()
            .filter(|(x,y)| *x >= 0 && *x < self.width as isize && *y >= 0 && *y < self.height as isize)
            .map(|(x,y)| (*x as usize, *y as usize))
            .collect()
    }

    fn print(&self) {
        println!("Width {}, Height {}", self.width, self.height);
        for i in 0..self.height{
            for j in 0..self.width {
                print!("{}", self.get(j,i));
            }
            println!("");
        }
    }

    fn print_path(&self, memo: &HashMap<(usize, usize), (Option<(usize,usize)>, usize)>) {
        let mut path = HashSet::new();
        let mut current = Some((self.width-1, self.height-1));

        while current.is_some() {
            path.insert(current.unwrap());
            current = memo[&current.unwrap()].0;
        }

        println!("Path {:?}", path);

        for y in 0..self.height {
            for x in 0..self.width {
                if path.contains(&(x,y)) {
                    print!("{}", self.get(x,y));
                } else {
                    print!("{}", '.');
                }
            }
            println!("");
        }
    }
}

fn helper(x: u8) -> u8 {
    if x <= 9 { x } else { x % 9 }
}

fn extend_line(line: Vec<u8>, multiplier: u8) -> Vec<u8> {
    line.iter().cycle()
        .zip((0..multiplier).flat_map(|m| iter::repeat(m).take(line.len())))
        .map(|(v,m)| helper(v+m))
        .collect()
}

fn read_input(multiplier :u8) -> Grid {
    let input_file = File::open("src/input.txt").unwrap();

    let reader = BufReader::new(input_file);
    let lines = reader.lines()
        .map(|x| x.unwrap())
        .collect::<Vec<String>>();

    let width = lines[0].len() * multiplier as usize;
    let height = lines.len() * multiplier as usize;

    let grid = lines.iter()
        .map(|l| l.chars().map(|x|x.to_digit(10).unwrap() as u8).collect())
        .map(|l| extend_line(l, multiplier))
        .flat_map(|l|l.into_iter())
        .collect();

    Grid::new(extend_line(grid, multiplier), width, height)
}

fn dijkstra(grid: &Grid) {
    let mut memo = HashMap::<(usize, usize), (Option<(usize,usize)>, usize)>::new();
    let mut to_visit = BinaryHeap::new();

    to_visit.push(HeapItem{pos: (0,0), dist: 0, prev: None});

    while let Some(current) = to_visit.pop() {
        if let Some(node) = memo.get(&current.pos) {
            if node.1 <= current.dist {
                continue;
            }
        }

        memo.insert(current.pos, (current.prev, current.dist));
        for n in grid.neighbors(current.pos.0, current.pos.1) {
            let pos = n;
            let prev = Some(current.pos);
            let dist = current.dist + grid.get(n.0, n.1);

            to_visit.push(HeapItem{pos, prev, dist});
        }
    }

    grid.print_path(&memo);
}

fn main() {
    println!("Reading input");
    //let input = read_input(1);
    let input = read_input(5);
    dijkstra(&input);
}
