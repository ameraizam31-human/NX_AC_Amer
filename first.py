import streamlit as st
import random

st.set_page_config(
    page_title="Guess The Number Game By Amer",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize all session state variables if they don't exist."""
    if 'secret_number' not in st.session_state:
        st.session_state.secret_number = None
    if 'attempts_count' not in st.session_state:
        st.session_state.attempts_count = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "Easy"
    if 'max_number' not in st.session_state:
        st.session_state.max_number = 50
    if 'guess_history' not in st.session_state:
        st.session_state.guess_history = []

def start_new_game():
    """Generate a new secret number and reset game state."""
    st.session_state.secret_number = random.randint(1, st.session_state.max_number)
    st.session_state.attempts_count = 0
    st.session_state.game_over = False
    st.session_state.guess_history = []

# Initialize session state on app load
initialize_session_state()

# Generate secret number if game hasn't started yet
if st.session_state.secret_number is None:
    start_new_game()

# =============================================================================
# SIDEBAR - DIFFICULTY SELECTION
# =============================================================================
with st.sidebar:
    st.header("⚙️ Game Settings")
    
    # Difficulty selection
    selected_difficulty = st.radio(
        "Select Difficulty:",
        options=["Easy (1-50)", "Hard (1-100)"],
        index=0 if st.session_state.difficulty == "Easy" else 1,
        help="Choose your difficulty level. Changing this will start a new game."
    )
    
    # Parse difficulty and max number
    new_difficulty = "Easy" if "Easy" in selected_difficulty else "Hard"
    new_max_number = 50 if new_difficulty == "Easy" else 100
    
    # Check if difficulty changed - if so, reset the game
    if new_difficulty != st.session_state.difficulty:
        st.session_state.difficulty = new_difficulty
        st.session_state.max_number = new_max_number
        start_new_game()
        st.rerun()
    
    st.divider()
    
    # Display game info
    st.info(f"🎯 Range: 1 to {st.session_state.max_number}")
    st.info(f"🔢 Difficulty: {st.session_state.difficulty}")
    
    # Hint section
    with st.expander("💡 Need a hint?"):
        st.write(f"The secret number is between 1 and {st.session_state.max_number}")
        st.write(f"You've made {st.session_state.attempts_count} attempt(s) so far.")
    
    st.divider()
    
    # Manual reset button
    if st.button("🔄 New Game", use_container_width=True):
        start_new_game()
        st.rerun()


st.title("🎮 Guess The Number Game By Amer")
st.subheader(f"I'm thinking of a number between 1 and {st.session_state.max_number}...")

# Game stats display using columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎯 Difficulty", st.session_state.difficulty)
with col2:
    st.metric("📝 Attempts", st.session_state.attempts_count)
with col3:
    st.metric("📊 Range", f"1 - {st.session_state.max_number}")

st.divider()

# =============================================================================
# GAME LOGIC
# =============================================================================

# Only show input if game is not over
if not st.session_state.game_over:
    st.subheader("Enter Your Guess")
    
    # Create columns for input and button
    input_col, button_col = st.columns([3, 1])
    
    with input_col:
        # Number input for user's guess
        user_guess = st.number_input(
            "Your guess:",
            min_value=1,
            max_value=st.session_state.max_number,
            value=1,
            step=1,
            key="guess_input",
            disabled=st.session_state.game_over
        )
    
    with button_col:
        # Add vertical spacing using empty writes
        st.write("")
        st.write("")
        submit_guess = st.button("🚀 Submit Guess", use_container_width=True)
    
    # Process the guess when submit button is clicked
    if submit_guess:
        # Increment attempt counter
        st.session_state.attempts_count += 1
        
        # Add to history
        st.session_state.guess_history.append(user_guess)
        
        # Check the guess
        if user_guess < st.session_state.secret_number:
            st.warning(f"📉 Too Low! The number is higher than {user_guess}")
            st.info("💡 Try a bigger number!")
            
        elif user_guess > st.session_state.secret_number:
            st.warning(f"📈 Too High! The number is lower than {user_guess}")
            st.info("💡 Try a smaller number!")
            
        else:
            # Correct guess!
            st.session_state.game_over = True
            
            # Trigger celebration
            st.balloons()
            
            # Display success message
            st.success(f"🎉 Congratulations! You guessed the number {st.session_state.secret_number}!")
            
            # Show attempts stats
            if st.session_state.attempts_count == 1:
                st.info("🏆 Incredible! You got it on the first try!")
            elif st.session_state.attempts_count <= 5:
                st.info(f"⭐ Great job! It took you {st.session_state.attempts_count} attempts.")
            else:
                st.info(f"👍 Good effort! You found it in {st.session_state.attempts_count} attempts.")
    
    # Show guess history
    if st.session_state.guess_history:
        st.divider()
        st.subheader("📜 Guess History")
        
        # Create a visual history with indicators
        history_cols = st.columns(min(len(st.session_state.guess_history), 10))
        for idx, guess in enumerate(st.session_state.guess_history):
            col_idx = idx % 10
            with history_cols[col_idx]:
                if guess < st.session_state.secret_number:
                    st.error(f"⬆️ {guess}")
                elif guess > st.session_state.secret_number:
                    st.error(f"⬇️ {guess}")
                else:
                    st.success(f"✅ {guess}")

else:
    # Game Over State - Show winning screen
    st.success(f"🎉 You Won! The number was {st.session_state.secret_number}")
    st.balloons()
    
    st.info(f"📊 Total Attempts: {st.session_state.attempts_count}")
    
    # Performance rating
    if st.session_state.attempts_count == 1:
        st.write("### 🏆 LEGENDARY! First try!")
    elif st.session_state.attempts_count <= 5:
        st.write("### ⭐ Excellent! You're a natural!")
    elif st.session_state.attempts_count <= 10:
        st.write("### 👍 Good Job! Well played!")
    else:
        st.write("### 💪 Not Bad! Keep practicing!")
    
    # Play Again button (prominent)
    st.divider()
    if st.button("🎮 Play Again", type="primary", use_container_width=True):
        start_new_game()
        st.rerun()

# =============================================================================
# FOOTER
# =============================================================================
st.divider()
st.caption("🎮 Guess the Number Game | Built with Streamlit | Have fun! 🎯")
