open System

let echo message =
    printfn "%s %d" message

[<EntryPoint>]
let main argv =
    let echo = echo "Foo"
    echo 4
    0 // return an integer exit code
