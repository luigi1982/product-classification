import math
import pandas as pd
from tqdm import tqdm
from transformers.pipelines.pt_utils import KeyDataset


def label(classifier, labels, hypothesis_template, ds, batch_size=8):

    results = []
    
    for output in tqdm(
        classifier(
            KeyDataset(ds, "product_name"),
            candidate_labels=labels,
            hypothesis_template=hypothesis_template,
            batch_size=batch_size
        ),
        total=len(ds)
    ):
        results.append(output)

    return results


def get_classes(ds, labels):

    classes = {
        'TP': [],
        'FP': [],
        'TN': [],
        'FN': []
    }

    for i, row in enumerate(ds):

        if labels[i] == row["manual_label"]:
            if labels[i]:
                classes["TP"].append(i)
            else:
                classes["TN"].append(i)

        else:
            if labels[i]:
                classes["FP"].append(i)
            else:
                classes["FN"].append(i)

    return classes


def label_and_eval(
        classifier, labels, hypothesis_template, ds, batch_size=8
    ):

    ### make sure the first label corresponds to is edible
    
    ### use the model to label the product names
    results = label(classifier, labels, hypothesis_template, ds, batch_size=batch_size)
    ### convert labels to bool
    edible = [r['labels'][0]==labels[0] for r in results]
    ### compute classes
    classes = get_classes(ds, edible)

    return {
        "classes": classes,
        "predicted": edible
    }
    