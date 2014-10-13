def saveMatrix(fMatrix, Matrix):
    FMatrix = open(fMatrix, 'w')
    for m_i in Matrix:
        tmpList = Matrix[m_i]
        tmpList = [str(l) for l in tmpList]
        tmpLine = ','.join(tmpList) + '\n'
        FMatrix.write(tmpLine)
    FMatrix.close()
        