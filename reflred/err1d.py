# This program is public domain

"""
Error propogation algorithms for simple arithmetic

Warning: like the underlying numpy library, the inplace operations
may return values of the wrong type if some of the arguments are
integers, so be sure to create them with floating point inputs.
"""
from __future__ import division  # Get true division

import numpy as np

def interp(X,Xp,Fp,varFp,left=None,right=None):
    """
    Linear interpolation of x points into points (xk,fk +/- dfk).

    xp is assumed to be monotonically increasing.  The interpolated
    value is undefined at duplicate points.

    left is (value,variance) to use for points before the range of xp, or
    None for the initial value.

    right is (value,variance) to use for points after the range of xp, or
    None for the final value.
    """
    idx = np.searchsorted(Xp[1:-1], X, side="right")
    # Support repeated values in Xp, which will lead to 0/0 errors if the
    # interpolated point is one of the repeated values.
    p = (Xp[idx+1]-X)/(Xp[idx+1]-Xp[idx])
    F = p*Fp[idx] + (1-p)*Fp[idx+1]
    varF = p**2*varFp[idx] + (1-p)**2*varFp[idx+1]
    #print p,F,varF,idx
    if left is None: left = Fp[0],varFp[0]
    if right is None: right = Fp[-1],varFp[-1]
    F[X<Xp[0]], varF[X<Xp[0]] = left
    F[X>Xp[-1]], varF[X>Xp[-1]] = right

    return F, varF

def div(X,varX, Y,varY):
    """Division with error propagation"""
    # Direct algorithm:
    #   Z = X/Y
    #   varZ = (varX/X**2 + varY/Y**2) * Z**2
    #        = (varX + varY * Z**2) / Y**2
    # Indirect algorithm to minimize intermediates
    Z = X/Y      # truediv => Z is a float
    varZ = Z**2  # Z is a float => varZ is a float
    varZ *= varY
    varZ += varX
    T = Y**2     # Doesn't matter if T is float or int
    varZ /= T
    return Z, varZ

def mul(X,varX, Y,varY):
    """Multiplication with error propagation"""
    # Direct algorithm:
    Z = X * Y
    varZ = Y**2 * varX + X**2 * varY
    # Indirect algorithm won't ensure floating point results
    #   varZ = Y**2
    #   varZ *= varX
    #   Z = X**2   # Using Z to hold the temporary
    #   Z *= varY
    #   varZ += Z
    #   Z[:] = X
    #   Z *= Y
    return Z, varZ

def sub(X,varX, Y, varY):
    """Subtraction with error propagation"""
    Z = X - Y
    varZ = varX + varY
    return Z, varZ

def add(X,varX, Y,varY):
    """Addition with error propagation"""
    Z = X + Y
    varZ = varX + varY
    return Z, varZ

def exp(X,varX):
    """Exponentiation with error propagation"""
    Z = np.exp(X)
    varZ = varX * Z**2
    return Z,varZ

def log(X,varX):
    """Logarithm with error propagation"""
    Z = np.log(X)
    varZ = varX / X**2
    return Z,varZ

def sin(X,varX):
    return np.sin(X), varX*np.cos(X)**2
def cos(X,varX):
    return np.cos(X), varX*np.sin(X)**2
def tan(X,varX):
    return np.tan(X), varX*np.sec(X)**2
def arcsin(X,varX):
    return np.arcsin(x), varX/(1-X**2)
def arccos(X,varX):
    return np.arccos(x), varX/(1-X**2)
def arctan(X,varX):
    return np.arctan(X), varX/(1+X**2)**2

def arctan2(X,varX, Y,varY):
    Z = np.arctan2(X,Y)
    varZ = div(X,varX, Y,varY)/(1+(X/Y)**2)**2
    return Z,varZ

# Confirm this formula before using it
# def pow(X,varX, Y,varY):
#    Z = X**Y
#    varZ = (Y**2 * varX/X**2 + varY * numpy.log(X)**2) * Z**2
#    return Z,varZ
#

def pow(X,varX,n):
    """X**n with error propagation"""
    # Direct algorithm
    #   Z = X**n
    #   varZ = n*n * varX/X**2 * Z**2
    # Indirect algorithm to minimize intermediates
    Z = X**n
    varZ = varX/X
    varZ /= X
    varZ *= Z
    varZ *= Z
    varZ *= n**2
    return Z, varZ

def pow2(X,varX, Y,varY):
    """X**Y with error propagation"""
    # Direct algorithm
    #   Z = X**Y
    #   varZ = Z**2 * ((Y*varX/X)**2 + (log(X)*varY)**2)
    Z = X**Y
    varZ = varX/X
    varZ *= Y
    varZ *= varZ
    T = np.log(X)
    T *= varY
    T *= T
    varZ += T
    del T
    varZ *= Z
    varZ *= Z
    return Z, varZ

def div_inplace(X,varX, Y,varY):
    """In-place division with error propagation"""
    # Z = X/Y
    # varZ = (varX + varY * (X/Y)**2) / Y**2 = (varX + varY * Z**2) / Y**2
    X /= Y     # X now has Z = X/Y
    T = X**2   # create T with Z**2
    T *= varY  # T now has varY * Z**2
    varX += T  # varX now has varX + varY*Z**2
    del T   # may want to use T[:] = Y for vectors
    T = Y   # reuse T for Y
    T **=2     # T now has Y**2
    varX /= T  # varX now has varZ
    return X,varX

def mul_inplace(X,varX, Y,varY):
    """In-place multiplication with error propagation"""
    # Z = X * Y
    # varZ = Y**2 * varX + X**2 * varY
    T = Y**2   # create T with Y**2
    varX *= T  # varX now has Y**2 * varX
    del T   # may want to use T[:] = X for vectors
    T = X   # reuse T for X**2 * varY
    T **=2     # T now has X**2
    T *= varY  # T now has X**2 * varY
    varX += T  # varX now has varZ
    X *= Y     # X now has Z
    return X,varX

def sub_inplace(X,varX, Y, varY):
    """In-place subtraction with error propagation"""
    # Z = X - Y
    # varZ = varX + varY
    X -= Y
    varX += varY
    return X,varX

def add_inplace(X,varX, Y,varY):
    """In-place addition with error propagation"""
    # Z = X + Y
    # varZ = varX + varY
    X += Y
    varX += varY
    return X,varX

def pow_inplace(X,varX,n):
    """In-place X**n with error propagation"""
    # Direct algorithm
    #   Z = X**n
    #   varZ = abs(n) * varX/X**2 * Z**2
    # Indirect algorithm to minimize intermediates
    varX /= X
    varX /= X     # varX now has varX/X**2
    X **= n       # X now has Z = X**n
    varX *= X
    varX *= X     # varX now has varX/X**2 * Z**2
    varX *= n**2  # varX now has varZ
    return X,varX

def pow2_inplace(X,varX, Y,varY):
    """X**Y with error propagation"""
    # Direct algorithm
    #   Z = X**Y
    #   varZ = Z**2 * ((Y*varX/X)**2 + (log(X)*varY)**2)
    varX /= X
    varX *= Y
    varX *= varX # varX now has (Y*varX/X)**2
    T = np.log(X)
    T *= varY
    T *= T
    varX += T # varX now has (Y*varX/X)**2 + (log(X)*varY)**2
    del T
    X **= Y   # X now has Z = X**Y
    varX *= X
    varX *= X # varX now has varZ
    return X, varX
