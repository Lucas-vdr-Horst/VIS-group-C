
function exs(source, path) {
    // Efficient XML Search

    if (source === undefined) {throw 'source is undefined'}
    let working_object = source;
    for (const tagName of path) {
        working_object = working_object.getElementsByTagName(tagName)[0]
    }
    return working_object
}
