import {calculate, Generations, Pokemon, Move} from '@smogon/calc';

const gen = Generations.get(5); // alternatively: const gen = 5;
const result = calculate(
  gen,
  new Pokemon(gen, 'Scyther', {
    item: 'Eviolite',
    nature: 'Jolly',
    evs: {atk: 252, spe: 252},
    boosts: {},
  }),
  new Pokemon(gen, 'Gengar', {
    item: 'Black Sludge',
    nature: 'Timid',
    evs: {spa: 252, spe: 252},
    boosts: {},
  }),
  new Move(gen, 'Sludge Bomb')
);

console.log(JSON.stringify(result))