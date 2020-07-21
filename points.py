import screen

# we assume a resolution of 1920x1080
pointsAllyLaneCardsActives = screen.createPointsAlongLine(34, 232, 1690, 724)
pointsAllyLaneCardsItems = screen.createPointsAlongLine(34, 232, 1690, 588)
pointsAllyImprovementsAndDeploy = screen.createPointsAlongLine(16, 473, 1440, 935)
pointsEnemyLaneCards = screen.createPointsAlongLine(14, 290, 1600, 362)
pointsEnemyImprovementsL = screen.createPointsAlongLine(7, 610, 824, 180)
pointsEnemyImprovementsR = screen.createPointsAlongLine(7, 1095, 1350, 180)
pointsHand = screen.createPointsAlongLine(20, 465, 1414, 1055)
pointsShop = screen.createPointsAlongLine(3, 690, 1110, 700)

points = {
	"a": pointsAllyLaneCardsActives + pointsAllyLaneCardsItems,
	"h": pointsHand,
	"k": pointsAllyImprovementsAndDeploy,
	"b": pointsEnemyLaneCards,
	"j": pointsEnemyImprovementsL + pointsEnemyImprovementsR,
	"s": pointsShop,
	"pp": screen.createPoint(1200, 834),
	"ll": screen.createPoint(18, 489),
	"lr": screen.createPoint(1901, 489),
	"sh": screen.createPoint(757, 290),
	"cl": screen.createPoint(795, 652),
	"pr": screen.createPoint(1100, 652),
	"pass": screen.createPoint(1570, 915),
}
