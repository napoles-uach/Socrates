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

def Socrates(prompt,n):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    #model="gpt-4",
    temperature=0.3,
    max_tokens=1000,

    messages=[{"role": "system", "content": f"You are Socrates, ask questions in a Socratic dialogue. Be critical with your Student, whenever possible check the operations as the student can make mistakes and correct him. If your Student gives a final answer, analyse the answer to see if it makes sense. Yo will have {n} chances to ask"},
              {"role": "user", "content": prompt},
              ]
  )

  return completion['choices'][0]['message']['content']

def Student(prompt,n):
  completion = openai.ChatCompletion.create(
    #model="gpt-3.5-turbo", 
    model="gpt-4",
    temperature=0.0,
    max_tokens=1000,

    messages=[{"role": "system", "content": f"You are a Cleaver Student. Try to answer the questions your mentor Socrates is asking you. Write your answer in a single sentence an wait for the following question. You will respond {n} questions."},
              {"role": "user", "content": prompt},
              ]
  )

  return completion['choices'][0]['message']['content']


problem = st.text_input("Enter your problem","The quadratic $3x^2-24x+72$ can be written in the form $a(x+b)^2+c$, where $a$, $b$, and $c$ are constants. What is $a+b+c$?")
with st.sidebar.expander("Examples", expanded=False):
    st.text(" 1) Bob can travel $m$ miles in $h$ hours on his bicycle. At this rate, how many hours would it take him to travel $h$ miles? Express your answer in terms of $m$ and $h$.")
    st.text("2) An equilateral triangle has all three of its vertices on the parabola $y=x^2-8x+5$. One vertex of the triangle is on the vertex of the parabola, and the opposite side lies along the line $y=k$. What is the value of $k$?")
    st.text("3) The shortest distance from the circle $x^2 + y^2 = 4x + 8y$ to the point $(5,-2)$ can be written in the form $\sqrt{m}$, where $m$ is an integer. Find $m$.")
    st.text("4) Heisenberg's Uncertainty Principle says that the product of the error in the measurement of a particle's momentum and the error in the measurement of a particle's position must be at least Planck's constant divided by $4\pi$. Suppose the error in the measurement of the momentum of a particle is halved. By how many percent does the minimum error in the measurement of its position increase?")

dialogue = problem + '\n'+"Socrates: "

boton = st.button('Run dialogue')
if boton:
    n=5
    for i in range(1,n+1):
        dialogue = dialogue + "Question "+str(i) + '\n'
        response = Socrates(f"Engage in a thorough Socratic dialogue to solve the problem. Generate only one question at a time  that explore the problem's context, variables, and relationships. Use this dialogue {dialogue} and continue with one single question",n )
        dialogue = dialogue +  response +'\n'
        st.info("Socrates: "+response)
        response = Student(f"Engage in a thorough Socratic dialogue to solve the problem. Generate only one answer at a time  that explore the problem's context, variables, and relationships. Use this dialogue {dialogue} and continue with one single answer.",n )
        st.success("Student: "+response)
        dialogue = dialogue + response + '\n'

        i+=1


st.sidebar.write('''
This app solves Math word problems by a dialogue between two agents,
one playing the role of "Socrates" (GPT-3-turbo) and the other as a "Student" (GPT-4).
This aproach is particularly useful for complex problems, where a single GPT model can fail.

Author: Jose M. Napoles-Duarte
@napoles3d
''')