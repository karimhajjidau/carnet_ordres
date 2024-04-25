# carnet_ordres
Simulateur de Carnet d’Ordres
Deux classes : OrderBook et Order

Deux types d'ordres :
- Ordre limite : l'ordre est passé à un prix précis par l'utilisateur
- Ordre au marché : l'ordre est passé à la meilleure offre ou à la meilleure demande. Nous n'éxectuons pas et ne stockons pas les ordres au marché s'ils ne conviennent pas.

Mécanisme de fixing :
- Nous réalisons un fixing au moment de la cloture et l'ouverture du marché. Le cours de fixing correspond au cours qui permet de maximiser le nombre de transactions 