// Return a value from a given range, which avoids zero, within a given tolerance.
function avoidZero(range, tolerance) {
    // Return a random value in the range from `-range` to strictly less than
    // `range`, excluding the inner range +/-`tolerance` (and, logically, zero as
    // well).
    let value = _.random(-range, range)
    while (-tolerance < value && value < tolerance) {
        value = _.random(-range, range)
    }
    return value
}
