"""

Adapting the Theano example ConvNet architecture for Google image scraping processing.

"""

from __future__ import print_function

import os
import sys
import timeit
import time

import numpy

from PIL import Image
import six.moves.cPickle as pickle

import theano
import theano.tensor as T
from theano.tensor.signal import pool
from theano.tensor.nnet import conv2d

from get_data import directory_to_dataset

from logistic_sgd import LogisticRegression, load_data
from mlp import HiddenLayer
from conv import LeNetConvPoolLayer

class TexturaNet(object):
    """
    Combination of a bunch of conv layers to produce a neural net!
    """

    def __init__(self, rng, input, image_shape,
        filter_shape1, filter_shape2, filter_shape3,
        poolsize=(2, 2), nkerns=(10, 15, 8), hidden_dim=50):
        """
        Allocate a LeNetConvPoolLayer with shared variable internal parameters.

        :type rng: numpy.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 4
        :param filter_shape: (number of filters, num input feature maps,
                              filter height, filter width)

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)

        :type poolsize: tuple or list of length 2
        :param poolsize: the downsampling (pooling) factor (#rows, #cols)
        """

        # Construct the first convolutional pooling layer:
        # filtering reduces the image size to (28-5+1 , 28-5+1) = (24, 24)
        # maxpooling reduces this further to (24/2, 24/2) = (12, 12)
        # 4D output tensor is thus of shape (batch_size, nkerns[0], 12, 12)

        self.layer1_input = input
        batch_size = input.shape[0]
        self.layer1 = LeNetConvPoolLayer(
            rng,
            input=self.layer1_input,
            image_shape=(batch_size, 1, image_shape[0], image_shape[1]),
            filter_shape=(nkerns[0], 1, filter_shape1[0], filter_shape1[1]),
            poolsize=poolsize
        )

        # Construct the second convolutional pooling layer
        # filtering reduces the image size to (12-5+1, 12-5+1) = (8, 8)
        # maxpooling reduces this further to (8/2, 8/2) = (4, 4)
        # 4D output tensor is thus of shape (batch_size, nkerns[1], 4, 4)

        image_shape2 = (
            (image_shape[0]-filter_shape1[0]+1)/poolsize[0],
            (image_shape[1]-filter_shape1[1]+1)/poolsize[1]
        )
        self.layer2 = LeNetConvPoolLayer(
            rng,
            input=self.layer1.output,
            image_shape=(batch_size, nkerns[0], image_shape2[0], image_shape2[1]),
            filter_shape=(nkerns[1], nkerns[0], filter_shape2[0], filter_shape2[1]),
            poolsize=poolsize
        )

        image_shape3 = (
            (image_shape2[0]-filter_shape2[0]+1)/poolsize[0],
            (image_shape2[1]-filter_shape2[1]+1)/poolsize[1]
        )
        self.layer3 = LeNetConvPoolLayer(
            rng,
            input=self.layer2.output,
            image_shape=(batch_size, nkerns[1], image_shape3[0], image_shape3[1]),
            filter_shape=(nkerns[2], nkerns[1], filter_shape3[0], filter_shape3[1]),
            poolsize=poolsize
        )

        self.layer4_input = self.layer3.output.flatten(2)
        image_shape4 = (
            (image_shape3[0]-filter_shape3[0]+1)/poolsize[0],
            (image_shape3[1]-filter_shape3[1]+1)/poolsize[1]
        )
        # construct a fully-connected sigmoidal layer
        self.layer4 = HiddenLayer(
            rng,
            input=self.layer4_input,
            n_in=nkerns[2] * image_shape4[0] * image_shape4[1],
            n_out=hidden_dim,
            activation=T.tanh
        )

        # classify the values of the fully-connected sigmoidal layer
        self.layer5 = LogisticRegression(input=self.layer4.output, n_in=hidden_dim, n_out=2)

        self.params = self.layer5.params + self.layer4.params + self.layer3.params + self.layer2.params + self.layer1.params




def train_images(adjective,dataset,nkerns=(10,15,8),learning_rate=0.1, n_epochs=50,
                    batch_size=1):
    """
    :type learning_rate: float
    :param learning_rate: learning rate used (factor for the stochastic
                          gradient)

    :type n_epochs: int
    :param n_epochs: maximal number of epochs to run the optimizer

    :type dataset: string
    :param dataset: path to the dataset used for training /testing (MNIST here)

    :type nkerns: list of ints
    :param nkerns: number of kernels on each layer
    """

    rng = numpy.random.RandomState(1000)

    datasets = directory_to_dataset(dataset)

    train_set_x, train_set_y = datasets[0]
    valid_set_x, valid_set_y = datasets[1]
    test_set_x, test_set_y = datasets[2]

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]
    
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]
    n_train_batches //= batch_size
    n_valid_batches //= batch_size
    n_test_batches //= batch_size
    print(n_valid_batches)

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch

    # start-snippet-1
    x = T.matrix('x')   # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print('... building the model')

    input = x.reshape((batch_size, 1, 128, 128))

    model = TexturaNet(
        rng,input,image_shape=(128, 128),
        filter_shape1=(9,9),filter_shape2=(5,5),filter_shape3=(5,5),
        poolsize=(2,2),nkerns=(10,15,8), hidden_dim=50
    );

    # the cost we minimize during training is the NLL of the model
    cost = model.layer5.negative_log_likelihood(y)

    # create a function to compute the mistakes that are made by the model
    test_model = theano.function(
        [index],
        model.layer5.errors(y),
        givens={
            x: test_set_x[index * batch_size: (index + 1) * batch_size],
            y: test_set_y[index * batch_size: (index + 1) * batch_size]
        }
    )

    validate_model = theano.function(
        [index],
        model.layer5.errors(y),
        givens={
            x: valid_set_x[index * batch_size: (index + 1) * batch_size],
            y: valid_set_y[index * batch_size: (index + 1) * batch_size]
        }
    )

    grads = T.grad(cost, model.params)

    updates = [
        (param_i, param_i - learning_rate * grad_i)
        for param_i, grad_i in zip(model.params, grads)
    ]

    train_model = theano.function(
        [index],
        cost,
        updates=updates,
        givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size],
            y: train_set_y[index * batch_size: (index + 1) * batch_size]
        }
    )
    # end-snippet-1

    ###############
    # TRAIN MODEL #
    ###############
    print('... training')
    # early-stopping parameters
    patience = 300  # look as this many examples regardless
    patience_increase = 2
    improvement_threshold = 0.95
    validation_frequency = min(n_train_batches, patience // 2)

    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = timeit.default_timer()

    epoch = 0
    done_looping = False

    while (epoch < n_epochs) and (not done_looping):
        epoch = epoch + 1
        for minibatch_index in range(n_train_batches):

            iter = (epoch - 1) * n_train_batches + minibatch_index

            if iter % 100 == 0:
                print('training @ iter = ', iter)
            cost_ij = train_model(minibatch_index)

            if (iter + 1) % validation_frequency == 0:

                # compute zero-one loss on validation set
                validation_losses = [validate_model(i) for i
                                     in range(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)
                print('epoch %i, minibatch %i/%i, validation error %f %%' %
                      (epoch, minibatch_index + 1, n_train_batches,
                       this_validation_loss * 100.))
                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:

                    #improve patience if loss improvement is good enough
                    if this_validation_loss < best_validation_loss *  \
                       improvement_threshold:
                        patience = max(patience, iter * patience_increase)

                    # save best validation score and iteration number
                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = [
                        test_model(i)
                        for i in range(n_test_batches)
                    ]
                    test_score = numpy.mean(test_losses)
                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

                    print(model.__dict__)
                    with open('../../cache/models/'+adjective+'.pkl', 'wb') as f:
                        pickle.dump(model, f)

            if patience <= iter:
                done_looping = True
                break

    end_time = timeit.default_timer()
    print('Optimization complete.')
    print('Best validation score of %f %% obtained at iteration %i, '
          'with test performance %f %%' %
          (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    print(('The code for file ' +
           os.path.split(__file__)[1] +
           ' ran for %.2fm' % ((end_time - start_time) / 60.)), file=sys.stderr)
    return True



def predict_image(model, image):
    """
    Predicts score for the image.
    """
    batch_size = 1

    model = pickle.load(open(model))
    img = numpy.asarray(Image.open(image).convert('L')).reshape((batch_size, 1, 128, 128))

    # compile a predictor function
    predict_model = theano.function(
        inputs=[model.layer1_input],
        outputs=model.layer5.y_pred)

    predicted_value = predict_model(img)
    print("Your image score is: " + str(predicted_value))
    return predicted_value


if __name__ == '__main__':
    """
    Usage:
        python texture_class.py train [images adjective]
    OR
        python texture_class.py predict [model image]
    """
    assert len(sys.argv) == 4
    if sys.argv[1] == 'train':
        if len(sys.argv) > 2:
            train_images(dataset=sys.argv[2], adjective=sys.argv[3])
        else:
            train_images(dataset=sys.argv[1])
    elif sys.argv[1] == 'predict':
        predict_image(sys.argv[2], sys.argv[3])

