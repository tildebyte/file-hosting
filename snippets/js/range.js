/*
Damn good JS implementation of Python's `range`, using ES6 Generator
Based on several partly-working ideas from SO
http://stackoverflow.com/questions/8273047/javascript-function-similar-to-python-range
http://stackoverflow.com/questions/3895478/does-javascript-have-a-method-like-range-to-generate-an-array-based-on-suppl
*/
let range = function * (start = 0, end = null, step = 1) {
    if (end === null) {
        end = start
        start = 0
    }
    let value = start
    while (value < end || end < value) {
        yield value
        value += step
    }
}
