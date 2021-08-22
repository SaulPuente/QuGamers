# QuGamers
Repository containing our project for the Qiskit Summer Jam 2021

# Team members
* Saúl Yael Puente Ruiz
* Ana Belén Jaime Cepeda

# Quantum Emblem
"Quantum Emblem" is a quantum strategy game inspired in the fantasy tactical role-playing game Fire Emblem. We modified the game's mechanics in order to take advantage of the quantum phenomena. We also added the possibility to add quantum logic gates to modify the soldiers' states. All this brings more tactics to the game, which will depend mainly on luck.

# How To Play
The objective of the gameis to kill all the soldiers in the enemy's army. Each army consists of 5 soldiers, each with 3 health points. The stats of a soldier appear in the white box when you click on it.

## Moves and attacks
The possible moves and attacks to make appear in blue and red respectively when you click an unit. You can skip a move and attack directly or skip both move and attack by clicking in the same soldier. You can only make one move and/or one attack per turn.

## How to apply quantum gates
Most of the gates can be simply applied by clicking a soldier, then pressing a key correspongind to a gate (H, X, Y, Z, R, M) and clicking the soldier again.
The hadamard gate adittionally needs to click to two empty squares of the possible moves.
You can select the angle of the Ry gate by tipyng the angle in the green box, the angle is set to 0 by default. You can also define the angle in terms of pi, for example:
0.5pi, 0.33pi, 2pi, 1.5pi, but not 5pi/3 or -2pi.
The M gate only takes effect when a soldier is in superposition, if this condition is satisfied the qubit will collapse to one state.

## Moves and attacks in superposition
When a soldier is in superposition you can only move one of the states per turn.
In the same way, you can only attack with one state per turn. Attacking when a soldier is in superposition is the funniest part of the game. The qubit automatically collapses when a soldier attacks, but it will only inflict damage if the soldier ends in the state that attacked. The same happens when a soldier in superposition is attacked, it will recive damage only if after collapsing the qubit the soldier ends in the state that is attacked.

## Showing the quantum circuit
You can see the quantum circuit of each army in the console or save the image to a file by pressing the key D.
