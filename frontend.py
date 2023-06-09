#front end
"""
frontkened for TicTacToe

"""

#   _____________   _____________   _____________
#   |XXX|XXX|XXX|   |   |XXX|   |   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#   |   |XXX|   |   |   |XXX|   |   |XXX|   |   |
#   -------------   -------------   -------------
#   |   |XXX|   |   |   |XXX|   |   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#
#   _____________   _____________   _____________
#   |XXX|XXX|XXX|   |XXX|XXX|XXX|   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#   |   |XXX|   |   |XXX|XXX|XXX|   |XXX|   |   |
#   -------------   -------------   -------------
#   |   |XXX|   |   |XXX|   |XXX|   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#
#   _____________   _____________   _____________
#   |XXX|XXX|XXX|   |XXX|XXX|XXX|   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#   |   |XXX|   |   |XXX|   |XXX|   |XXX|XXX|   |
#   -------------   -------------   -------------
#   |   |XXX|   |   |XXX|XXX|XXX|   |XXX|XXX|XXX|
#   -------------   -------------   -------------
#

import streamlit as st
import backend as backend

# styling
st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# TIC TAC TOE"
    }
)
#---- HEADER SECTION ----
with st.container():
    #st.subheader("Project 1 by Sofia Torres, Stephanie Seanz, and Mia Marte 👋")
    st.title(":x: :blue[Tic-Tac-Toe Game :o: ] ")
    st.markdown("_Project 1 by Sofia Torres, Stephanie Seanz, and Mia Marte_ "    )
    st.write("The purpose of this game is to interact with an AI generator and try to win against it.\n"
             "Do you think you have the capabilities to win against a randomn AI?\n "
             "\nHope you enjoy our game!\n")


#---- ABOUT US ----
with st.container():
    st.write("---")

color = st.select_slider(
    'Difficulty level',
    options=['easy', 'medium', 'hard'])





# initialize session_state
if 't' not in st.session_state: st.session_state.t = None
if 'result' not in st.session_state: st.session_state.result  = backend.GameState.Ongoing
if 'winner' not in st.session_state: st.session_state.winner = backend.Player.Blank
if 'AIWin' not in st.session_state: st.session_state.AIWin = 0
if 'HumanWin' not in st.session_state: st.session_state.HumanWin = 0
if 'Draw' not in st.session_state: st.session_state.Draw = 0


if st.session_state.t == None:
    choice = st.selectbox('Who starting the game?', ["Please select", "Random AI", "YOU"])
    if choice == "Random AI":
        st.session_state.t = backend.TicTacToe(symbolAI='X', symbolHuman='O', firstPlayer=backend.Player.AI)
        st.experimental_rerun()
    elif choice == "YOU":
        st.session_state.t = backend.TicTacToe(symbolAI='O', symbolHuman='X', firstPlayer=backend.Player.Human)
        st.experimental_rerun()
else:
    # check for end condition
    st.session_state.result, st.session_state.winner = st.session_state.t.checkWinner()

    def callback(row, col):
        # on button click, playerMove
        if st.session_state.t.currentPlayer == backend.Player.Human:
            st.session_state.t.playerMove(row, col)
            st.session_state.t.currentPlayer = backend.Player.AI

    def reset():    
        for key in st.session_state.keys():
            if key != 'Draw' and key != 'AIWin' and key != 'HumanWin':
                del st.session_state[key]
        st.experimental_rerun()


    c = st.empty()
    with c.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            r1c1 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[0][0]], key='r1c1', on_click=callback, args=(0, 0))
            r2c1 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[1][0]], key='r2c1', on_click=callback, args=(1, 0))
            r3c1 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[2][0]], key='r3c1', on_click=callback, args=(2, 0))
        with col2:
            r1c2 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[0][1]], key='r1c2', on_click=callback, args=(0, 1))
            r2c2 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[1][1]], key='r2c2', on_click=callback, args=(1, 1))
            r3c2 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[2][1]], key='r3c2', on_click=callback, args=(2, 1))
        with col3:
            r1c3 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[0][2]], key='r1c3', on_click=callback, args=(0, 2))
            r2c3 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[1][2]], key='r2c3', on_click=callback, args=(1, 2))
            r3c3 = st.button(label=st.session_state.t.symbolMap[st.session_state.t.board[2][2]], key='r3c3', on_click=callback, args=(2, 2))

        if st.button("Reset"): reset()


    if st.session_state.result != backend.GameState.Ongoing:
            
            if st.session_state.winner != backend.Player.Blank:
            
                if st.session_state.winner == backend.Player.Human: 
                    st.success('You win. Yay!')
                    st.balloons()
                    st.session_state.HumanWin += 1
            
                elif st.session_state.winner == backend.Player.AI: 
                    st.error('The AI wins!')
                    st.balloons()
                    st.session_state.AIWin += 1
            
            else: 
                st.info('A tie has been drawn.')
                st.session_state.Draw += 1

    else:
        st.info('There is a game in progress. How exciting!')
        if  st.session_state.t.currentPlayer  == backend.Player.AI:
            with st.spinner('AI is finding its next move...'):
                # AI Move and label button accordingly
                st.session_state.t.bestMove()
                st.session_state.t.currentPlayer = backend.Player.Human
                # rerunning the app to trigger checkWinner() process
            st.success("Done!")
            st.experimental_rerun()
