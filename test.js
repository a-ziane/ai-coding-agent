const numbers = [10, 20, 30];
const average = numbers.reduce((total, number) => total + number, 0)
    / numbers.length;

console.log(average);