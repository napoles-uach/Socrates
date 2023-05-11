import openai
import os
import streamlit as st
st.set_page_config(
    page_title="Socrates",
    layout="wide",
)
# Get the API key for the OpenAI API.
openai.api_key = os.environ["gptkey"]

st.title("Socratic Dialog for Solving Math Word Problems")
sys_prompt=st.sidebar.text_input("System Prompt for Socrates","You are Socrates, ask questions in a Socratic dialogue. Be critical with your Student, whenever possible check the operations as the student can make mistakes and correct him. If your Student gives a final answer, analyse the answer to see if it makes sense. Yo will have 5 chances to ask")
def Socrates(prompt,n,model,sysprompt):
  completion = openai.ChatCompletion.create(
    model=model,
    #model="gpt-3.5-turbo", 
    #model="gpt-4",
    temperature=0.3,
    max_tokens=1000,

    messages=[{"role": "system", "content": sysprompt},
              {"role": "user", "content": prompt},
              ]
  )

  return completion['choices'][0]['message']['content']

def Student(prompt,n,model):
  completion = openai.ChatCompletion.create(
    model=model,
    #model="gpt-3.5-turbo", 
    #model="gpt-4",
    temperature=0.0,
    max_tokens=1000,

    messages=[{"role": "system", "content": f"You are a Cleaver Student. Try to answer the questions your mentor Socrates is asking you. Write your answer in a single sentence an wait for the following question. You will respond {n} questions."},
              {"role": "user", "content": prompt},
              ]
  )

  return completion['choices'][0]['message']['content']

text_example = '''Una liebre y una tortuga compiten en una carrera en una ruta 
de 1.00 km de largo. La tortuga paso a paso continuo y de 
manera estable a su máxima rapidez de 0.200 m/s se dirige 
hacia la línea de meta. La liebre corre a su máxima rapidez de 
8.00 m/s hacia la meta durante 0.800 km y luego se detiene 
para fastidiar a la tortuga. ¿Cuán cerca de la meta la liebre 
puede dejar que se acerque la tortuga antes de reanudar la 
carrera, que gana la tortuga en un final de fotografía? Suponga 
que ambos animales, cuando se mueven, lo hacen de manera 
constante a su respectiva rapidez máxima.'''
problem = st.text_input("Enter your problem",text_example)
with st.sidebar.expander("Examples", expanded=False):
    st.text(" 1) The quadratic $3x^2-24x+72$ can be written in the form $a(x+b)^2+c$, where $a$, $b$, and $c$ are constants. What is $a+b+c$?")
    st.text("2) An equilateral triangle has all three of its vertices on the parabola $y=x^2-8x+5$. One vertex of the triangle is on the vertex of the parabola, and the opposite side lies along the line $y=k$. What is the value of $k$?")
    st.text("3) The shortest distance from the circle $x^2 + y^2 = 4x + 8y$ to the point $(5,-2)$ can be written in the form $\sqrt{m}$, where $m$ is an integer. Find $m$.")
    st.text("4) Heisenberg's Uncertainty Principle says that the product of the error in the measurement of a particle's momentum and the error in the measurement of a particle's position must be at least Planck's constant divided by $4\pi$. Suppose the error in the measurement of the momentum of a particle is halved. By how many percent does the minimum error in the measurement of its position increase?")

dialogue = problem + '\n'+"Socrates: "
modelSoc=st.selectbox('model for Socrates',['gpt-3.5-turbo','gpt-4'])
modelEst=st.selectbox('model for Student',['gpt-3.5-turbo','gpt-4'])
boton = st.button('Run dialogue')
if boton:
    n=5
    for i in range(1,n+1):
        dialogue = dialogue + "Question "+str(i) + '\n'
        response = Socrates(f"Engage in a thorough Socratic dialogue to solve the problem. Generate only one question at a time  that explore the problem's context, variables, and relationships. Use this dialogue {dialogue} and continue with one single question",n,modelSoc,sys_prompt )
        dialogue = dialogue +  response +'\n'
        st.info("Socrates: "+response)
        response = Student(f"Engage in a thorough Socratic dialogue to solve the problem. Generate only one answer at a time  that explore the problem's context, variables, and relationships. Use this dialogue {dialogue} and continue with one single answer.",n,modelEst )
        st.success("Student: "+response)
        dialogue = dialogue + response + '\n'

        i+=1


st.sidebar.write('''
This app solves Math word problems by a dialogue between two agents,
one playing the role of "Socrates" (GPT-3-turbo) and the other as a "Student" (GPT-4).
This aproach is particularly useful for complex problems, where a single GPT model can fail.

Author: Jose M. Napoles-Duarte
''')
