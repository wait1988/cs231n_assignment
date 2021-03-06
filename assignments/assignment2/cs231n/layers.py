import numpy as np

def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) where x[i] is the ith input.
  We multiply this against a weight matrix of shape (D, M) where
  D = \prod_i d_i

  Inputs:
  x - Input data, of shape (N, d_1, ..., d_k)
  w - Weights, of shape (D, M)
  b - Biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  reshapeX = x.reshape(x.shape[0],np.prod(x.shape[1:]))
  out = reshapeX.dot(w)+b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  reshapeX = x.reshape(x.shape[0],np.prod(x.shape[1:]))
  dw = reshapeX.T.dot(dout)
  dx = dout.dot(w.T)
  db = np.sum(dout,axis=0)
  dx = dx.reshape(x.shape)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.where(x>0,x,0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = dout*np.where(x>0,1,0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx

def padwithzero(vector,pad_width,iaxis,kwargs):
  vector[:pad_width[0]] = 0
  vector[-pad_width[1]:] = 0
  return vector

def pad_matrix(x,pad):
  X_pad = np.zeros((x.shape[0],x.shape[1],x.shape[2]+2*pad,x.shape[3]+2*pad))
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      X_pad[i,j,:,:] = np.lib.pad(x[i,j,:,:],pad,padwithzero)
  return X_pad

def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  N,C,H,W = x.shape
  F,C,HH,WW = w.shape
  pad = conv_param['pad']
  stride = conv_param['stride']
  W_row = w.reshape(w.shape[0],np.prod(w.shape[1:]))
  Hs = 1 + (x.shape[2]+2*pad-w.shape[2])/stride
  Ws = 1 + (x.shape[3]+2*pad-w.shape[3])/stride
  X_col = np.zeros((np.prod(w.shape[1:]),Hs*Ws*x.shape[0]))
  X_pad = np.pad(x,[(0,0),(0,0),(pad,pad),(pad,pad)],'constant')  
  for i in range(N):
    for j in range(Hs):
      for k in range(Ws):
        X_col[:,i*Hs*Ws+j*Ws+k] = X_pad[i,:,j*stride:j*stride+HH,k*stride:k*stride+WW].flatten()

  ans = (W_row.dot(X_col).T + b).T.reshape(F,N,Hs,Ws)
  out = np.transpose(ans,(1,0,2,3))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, X_col,X_pad,conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  (x, w, b, X_col, X_pad,conv_param) = cache
  N,C,H,W = x.shape
  F,C,HH,WW = w.shape
  pad = conv_param['pad']
  stride = conv_param['stride']
  #W_row = w.reshape(w.shape[0],np.prod(w.shape[1:]))
  W_row = w.reshape(w.shape[0],-1)
  Hs = 1 + (x.shape[2]+2*pad-w.shape[2])/stride
  Ws = 1 + (x.shape[3]+2*pad-w.shape[3])/stride
  db = np.sum(dout,axis=(0,2,3))
  dout_s = np.transpose(dout,(1,0,2,3))
  dout_re = dout_s.reshape((dout_s.shape[0],-1))
  dw = dout_re.dot(X_col.T).reshape(w.shape)
  dx_col = W_row.T.dot(dout_re)
  dx_pad = np.zeros(X_pad.shape)
  for i in range(N):
    for j in range(Hs):
      for k in range(Ws):
        ##########IMPORTANT!!#################
        #dx_pad += dx_col, not dx_pad = dx_col
        ######################################
        dx_pad[i,:,j*stride:j*stride+HH,k*stride:k*stride+WW] += dx_col[:,i*Hs*Ws+j*Ws+k].reshape(C,HH,WW)  
  
  dx = dx_pad[:,:,pad:-pad,pad:-pad]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db

def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  ph = pool_param['pool_height']
  pw = pool_param['pool_width']
  ps = pool_param['stride']
  N,C,H,W = x.shape
  Hs = (H - ph)/ps + 1
  Ws = (W - pw)/ps + 1
  x_col = np.zeros((N*C*Hs*Ws,ph*pw))
  for i in range(N):
    for j in range(C):
      for k in range(Hs):
        for t in range(Ws):
          x_col[i*C*Hs*Ws+j*Hs*Ws+k*Ws+t,:] = x[i,j,k*ps:k*ps+ph,t*ps:t*ps+pw].flatten()
  
  x_col_max = np.max(x_col,axis=1)
  out = x_col_max.reshape(N,C,Hs,Ws)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, x_col, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x, x_col, pool_param = cache
  ph = pool_param['pool_height']
  pw = pool_param['pool_width']
  ps = pool_param['stride']
  N,C,H,W = x.shape
  Hs = (H - ph)/ps + 1
  Ws = (W - pw)/ps + 1
  x_idx_max = np.argmax(x_col,axis=1)
  dx_col = np.zeros(x_col.shape)
  dx_col[range(x_col.shape[0]),x_idx_max] = dout.reshape((np.prod(dout.shape[:]),))[range(x_col.shape[0])]
  dx = np.zeros(x.shape)
  for i in range(N):
    for j in range(C):
      for k in range(Hs):
        for t in range(Ws):
          dx[i,j,k*ps:k*ps+ph,t*ps:t*ps+pw] = dx_col[i*C*Hs*Ws+j*Hs*Ws+k*Ws+t,:].reshape(ph,pw)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx

