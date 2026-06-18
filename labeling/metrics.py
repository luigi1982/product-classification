from sklearn import metrics
from collections import Counter
from matplotlib import pyplot as plt

### implementation of metrics as Accuracy, Precision, Specifity and Sensitivity
### visulization through a confusion matrix


def accuracy(classes):

    '''
        accuracy:
        returns the percentage of samples that have been classified correctly
    '''

    return (len(classes['TP']) + len(classes['TN'])) / sum(len(classes[c]) for c in list(classes.keys()))


def precision(classes):
  
    '''
        precision:
        returns the percentage of samples that have been accurately classified as positive by the model
    '''

    return len(classes['TP']) / (len(classes['TP']) + len(classes['FP']) + 1e-5)


def sensitivity(classes):
  
    '''
        sensitivity:
        returns the percentage of positive samples that have been detected by the model
    '''

    return len(classes['TP']) / (len(classes['TP']) + len(classes['FN']) + 1e-5)


def specificity(classes):

    '''
        specifity:
        returns the percentage of negative samples that have been correctly detected by the model
    '''

    return len(classes['TN']) / (len(classes['TN']) + len(classes['FP']) + 1e-5)


def return_all_metrics(classes):

    """
        return all of the metrics
    """

    acc, prec, sens, spec = accuracy(classes), precision(classes), sensitivity(classes), specificity(classes)

    return {
        "accuracy": acc,
        "precision": prec,
        "sensitivity": sens,
        "specifity": spec
    }


def most_common_words(series, n=50):
    counter = Counter()
    for text in series:
        counter.update(str(text).split())
    return counter.most_common(n)


def most_common_fp(ds, classes):

    fps = list(ds["product_name"][classes["FP"]])
    return most_common_words(fps)


def most_common_fn(ds, classes):
    fns = list(ds["product_name"][classes["FN"]])
    return most_common_words(fns)


def show_words(counter):

    plt.figure(figsize=(15, 3))
    plt.bar([w[0] for w in counter[:10]], [w[1] for w in counter[:10]])


def confusion_matrix(labels, predicted):

    confusion_matrix = metrics.confusion_matrix(labels, predicted)
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [0, 1])
    cm_display.plot()