js_string = "import {{calculate, Generations, Pokemon, Move}} from '@smogon/calc';" \
            "\n\nconst gen = Generations.get({}); // alternatively: const gen = 5;" \
            "\nconst result = calculate(" \
            "\n  gen," \
            "\n  new Pokemon(gen, '{}', {{" \
            "\n    item: '{}'," \
            "\n    nature: '{}'," \
            "\n    evs: {}," \
            "\n    boosts: {}," \
            "\n  }})," \
            "\n  new Pokemon(gen, '{}', {{" \
            "\n    item: '{}'," \
            "\n    nature: '{}'," \
            "\n    evs: {}," \
            "\n    boosts: {}," \
            "\n  }})," \
            "\n  new Move(gen, '{}')" \
            "\n);" \
            "\n" \
            "\nconsole.log(JSON.stringify(result))"
