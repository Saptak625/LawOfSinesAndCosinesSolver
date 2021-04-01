import sys
import math

degreeMode = 'd' in input("MODE: ").lower()
anglesInputs = []
sidesInputs = []
for i in range(3):
  sidesInputs.append(float(input("Side "+chr(ord('a')+i)+": ")))
  angle = float(input("Angle "+chr(ord('A')+i)+": "))
  if degreeMode:
    angle = math.radians(angle)
  anglesInputs.append(angle)

if len([i for i in anglesInputs if i > 0] + [i for i in sidesInputs if i > 0]) != 3:
  print("Not enough or too many inputs.")
  sys.exit(0)

#Operation and Steps
def solveForSide(angle1, side1, angle2):
  return (side1 * math.sin(angle2))/math.sin(angle1)

def solveForAngle(angle1, side1, side2):
  try:
    referenceAngle = math.asin((side2 * math.sin(angle1))/side1)
    return [referenceAngle if referenceAngle >= 0 else math.radians(360)-referenceAngle, math.radians(180)-referenceAngle]
  except:
    return [0.0, 0.0]

class Triangle:
  pairIndex = None
  originalPair = None
  def __init__(self, anglesInputs, sidesInputs):
    self.anglesInputs = anglesInputs[:]
    self.sidesInputs = sidesInputs[:]
    self.solved = False
  
  def set(pair, index):
    Triangle.pairIndex = index
    Triangle.originalPair = pair

  def solve(self):
    #Iterate and Solve for each angle
    solved = []
    iteration = 1
    while len(solved) != 2 or iteration < 2:
      solved = []
      for i in range(3):
        if i != Triangle.pairIndex:
          #Check which measurement is missing
          if self.anglesInputs[i] > 0:
            #Side Missing
            self.sidesInputs[i] = solveForSide(Triangle.originalPair[0], Triangle.originalPair[1], self.anglesInputs[i])
          elif self.sidesInputs[i] > 0:
            #Angle Missing
            possibleList = solveForAngle(Triangle.originalPair[0], Triangle.originalPair[1], self.sidesInputs[i])
            self.anglesInputs[i] = possibleList[0]
            copy = self.copy()
            copy.anglesInputs[i] = possibleList[1]
            solveQueue.append(copy)
          else:
            continue
          solved.append(i)
      if len(solved) == 1:
        thirdAngle = math.radians(180) - sum([i for i in self.anglesInputs if i > 0])
        self.anglesInputs = [i if i > 0 else thirdAngle for i in self.anglesInputs]
      iteration += 1
    self.solved = True

  def checkIfTriangle(self):
    angleTest = round(math.radians(180), 4) == round(sum(self.anglesInputs), 4)
    a = self.sidesInputs[0]
    b = self.sidesInputs[1]
    c = self.sidesInputs[2]
    if (a + b <= c) or (a + c <= b) or (b + c <= a) or not angleTest:
        return False
    else:
        return True

  def displayAnswer(self):
    if self.checkIfTriangle():
      #Convert to Degrees
      if degreeMode:
        convertedAngles = [math.degrees(i) for i in self.anglesInputs]
      #Display Answers
      for i in range(3):
        print("Side "+chr(ord('a')+i)+":", round(self.sidesInputs[i], 4))
        print("Angle "+chr(ord('A')+i)+":", round(convertedAngles[i], 4))
      print()

  def copy(self):
    copyTriangle = Triangle(anglesInputs, sidesInputs)
    copyTriangle.anglesInputs = self.anglesInputs[:]
    copyTriangle.sidesInputs = self.sidesInputs[:]
    copyTriangle.solved = self.solved
    return copyTriangle
solveQueue = [Triangle(anglesInputs, sidesInputs)]
try:
  pairIndex = [i for i in range(3) if sidesInputs[i] > 0 and anglesInputs[i] > 0][0]
  originalPair = [anglesInputs[pairIndex], sidesInputs[pairIndex]]
  Triangle.set(originalPair, pairIndex)
  index = 0
  print("\nFinal Answer:")
  solution = False
  while index < len(solveQueue):
    solveQueue[index].solve()
    if solveQueue[index].checkIfTriangle():
      solution = True
    solveQueue[index].displayAnswer()
    index += 1
  if not solution:
    print("No Solution Found.")
except IndexError:
  print("Need at least 1 angle or side.")
  sys.exit(0)