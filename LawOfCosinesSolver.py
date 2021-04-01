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

def getOtherCorrespondingSides(angleIndex, sides):
  return [sides[i] for i in range(3) if i != angleIndex]

correspondingCheck = False
for i in range(3):
  check = True
  for val in getOtherCorrespondingSides(i, sidesInputs):
    if val <= 0:
      check = False
  if check:
    correspondingCheck = True
if not correspondingCheck:
  print("Needs to follow Law of Cos format.")
  sys.exit(0)

#Operation and Steps
def solveForSide(sideIndex, angles, sides):
  otherSides = getOtherCorrespondingSides(sideIndex, sides)
  correspondingAngle = angles[sideIndex]
  return math.sqrt((otherSides[0]*otherSides[0])+(otherSides[1]*otherSides[1])-(2*otherSides[0]*otherSides[1])*math.cos(correspondingAngle))

def solveForAngle(angleIndex, angles, sides):
  c = sides[angleIndex]
  otherSides = getOtherCorrespondingSides(angleIndex, sides)
  try:
    referenceAngle = math.acos(((otherSides[0]*otherSides[0])+(otherSides[1]*otherSides[1])-(c*c))/(2*otherSides[0]*otherSides[1]))
    return referenceAngle
  except ValueError:
    return [0.0]

class Triangle:
  def __init__(self, anglesInputs, sidesInputs):
    self.anglesInputs = anglesInputs[:]
    self.sidesInputs = sidesInputs[:]
    self.solved = False

  def solve(self):
    #Iterate and Solve for each angle
    solved = []
    iteration = 1
    while len(solved) != 2 and iteration < 3:
      solved = []
      for i in range(3):
        #Check which measurement is missing
        if self.sidesInputs[i] <= 0:
          #Side Missing
          self.sidesInputs[i] = solveForSide(i, self.anglesInputs, self.sidesInputs)
          solved.append(i)
        if self.anglesInputs[i] <= 0:
          #Angle Missing
          c = self.sidesInputs[i]
          otherSides = getOtherCorrespondingSides(i, self.sidesInputs)
          if c > 0 and len([i for i in otherSides if i <= 0]) == 0:
            self.anglesInputs[i] = solveForAngle(i, self.anglesInputs, self.sidesInputs)
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