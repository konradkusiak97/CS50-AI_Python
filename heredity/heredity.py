import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    multValues = dict()
    zero_gene = set(people.keys()) - (one_gene|two_genes)

    for person in zero_gene:
        if person in have_trait:
            trait = PROBS['trait'][0][True]
        else:
            trait = PROBS['trait'][0][False]
        if people[person]['mother'] == None:
            prob = PROBS['gene'][0]
            prob *= trait
            multValues[person] = prob
        else:
            mother = people[person]['mother']
            father = people[person]['father']
            if mother in one_gene and father in one_gene:
                # The only way child will get 0 genes is if mum will give none with probability
                # 0.5 + 0.01 and dad will give none with 0.5 + 0.01
                probM = probF = 0.5 + PROBS['mutation']
                prob = probM*probF*trait
                multValues[person] = prob
            elif mother in two_genes and father in two_genes:
                # child will get 0 genes if mother and father will give zero genes
                # the probability is mutation from mother * mutation from father
                probM = probF = PROBS['mutation']
                prob = probF*probM*trait
                multValues[person] = prob
            elif mother in zero_gene and father in zero_gene:
                # only if none of parents will give the gene, 0.99 * 0.99
                probM = probF = 1 - PROBS['mutation']
                prob = probM*probF*trait
                multValues[person] = prob
            elif (mother in one_gene and father in two_genes) or (mother in two_genes and father in one_gene):
                prob1 = 0.5 + PROBS['mutation']
                prob2 = PROBS['mutation']
                prob = prob1*prob2*trait
                multValues[person] = prob
            elif (mother in zero_gene and father in two_genes) or (mother in two_genes and father in zero_gene):
                prob0 = 1 - PROBS['mutation']
                prob2 = PROBS['mutation']
                prob = prob0*prob2*trait
                multValues[person] = prob
            elif (mother in zero_gene and father in one_gene) or (mother in one_gene and father in zero_gene):
                prob0 = 1 - PROBS['mutation']
                prob1 = 0.5 + PROBS['mutation']
                prob = prob0*prob1*trait
                multValues[person] = prob
    
    for person in one_gene:
        if person in have_trait:
            trait = PROBS['trait'][1][True]
        else:
            trait = PROBS['trait'][1][False]
        if people[person]['mother'] == None:
            prob = PROBS['gene'][1]
            prob *= trait
            multValues[person] = prob
        else:
            mother = people[person]['mother']
            father = people[person]['father']

            if mother in one_gene and father in one_gene:
                probM = 0.5 - PROBS['mutation']
                probF = 0.5 + PROBS['mutation']
                prob = 2*probM*probF*trait
                multValues[person] = prob

            elif mother in two_genes and father in two_genes:
                probM = 1 - PROBS['mutation']
                probF = PROBS['mutation']
                prob = 2*probF*probM*trait
                multValues[person] = prob

            elif mother in zero_gene and father in zero_gene:
                probM = PROBS['mutation']
                probF = 1 - PROBS['mutation']
                prob = 2*probM*probF*trait
                multValues[person] = prob

            elif (mother in one_gene and father in two_genes) or (mother in two_genes and father in one_gene):
                prob1 = [0.5 - PROBS['mutation'], 0.5 + PROBS['mutation']]
                prob2 = [PROBS['mutation'], 1-PROBS['mutation']]
                prob = (prob1[0]*prob2[0] + prob1[1]*prob2[1])*trait
                multValues[person] = prob

            elif (mother in zero_gene and father in two_genes) or (mother in two_genes and father in zero_gene):
                prob0 = [PROBS['mutation'], 1-PROBS['mutation']]
                prob2 = [PROBS['mutation'], 1-PROBS['mutation']]
                prob = (prob0[0]*prob2[0]+prob0[1]*prob2[1])*trait
                multValues[person] = prob

            elif (mother in zero_gene and father in one_gene) or (mother in one_gene and father in zero_gene):
                prob0 = [PROBS['mutation'], 1-PROBS['mutation']]
                prob1 = [0.5+PROBS['mutation'], 0.5-PROBS['mutation']]
                prob = (prob0[0]*prob1[0]+prob0[1]*prob1[1])*trait
                multValues[person] = prob

    for person in two_genes:
        if person in have_trait:
            trait = PROBS['trait'][2][True]
        else:
            trait = PROBS['trait'][2][False]
        if people[person]['mother'] == None:
            prob = PROBS['gene'][2]
            prob *= trait
            multValues[person] = prob
        else:
            mother = people[person]['mother']
            father = people[person]['father']

            if mother in one_gene and father in one_gene:
                probM = 0.5 - PROBS['mutation']
                probF = 0.5 - PROBS['mutation']
                prob = probM*probF*trait
                multValues[person] = prob

            elif mother in two_genes and father in two_genes:
                probM = 1 - PROBS['mutation']
                probF = 1 - PROBS['mutation']
                prob = probF*probM*trait
                multValues[person] = prob

            elif mother in zero_gene and father in zero_gene:
                probM = PROBS['mutation']
                probF = PROBS['mutation']
                prob = probM*probF*trait
                multValues[person] = prob

            elif (mother in one_gene and father in two_genes) or (mother in two_genes and father in one_gene):
                prob1 = 0.5-PROBS['mutation']
                prob2 = 1-PROBS['mutation']
                prob = prob1*prob2*trait
                multValues[person] = prob

            elif (mother in zero_gene and father in two_genes) or (mother in two_genes and father in zero_gene):
                prob0 = PROBS['mutation']
                prob2 = 1-PROBS['mutation']
                prob = prob0*prob2*trait
                multValues[person] = prob

            elif (mother in zero_gene and father in one_gene) or (mother in one_gene and father in zero_gene):
                prob0 = PROBS['mutation']
                prob1 = 0.5-PROBS['mutation']
                prob = prob0*prob1*trait
                multValues[person] = prob

    result = 1
    for v in list(multValues.values()):
        result *= v
    return result

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    zero_gene = set(probabilities.keys()) - (one_gene|two_genes)

    for person in one_gene:
        probabilities[person]['gene'][1] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p

    for person in two_genes:
        probabilities[person]['gene'][2] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p

    for person in zero_gene:
        probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        s = probabilities[person]['gene'][0]+probabilities[person]['gene'][1]+probabilities[person]['gene'][2]
        for i in range(3):
            probabilities[person]['gene'][i] /= s

        s = probabilities[person]['trait'][False] + probabilities[person]['trait'][True]
        probabilities[person]['trait'][False] /= s
        probabilities[person]['trait'][True] /= s


if __name__ == "__main__":
    main()
