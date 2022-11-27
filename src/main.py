import init_game
import generate_field
import calculate_path
import do_move


#inicialize juego
execfile('init_game.py')
print('juego inicializado, imagen tomada')
#genere field
execfile('generate_field.py')
print('campo generado')
#calcule path
execfile('calculate_path.py')
print('path calculado')
#ejecute movimientos juego
print('pilas corra al juego para ejecutar el path')
execfile('do_move.py')
