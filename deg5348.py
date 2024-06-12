#!/usr/bin/env python
# coding: utf-8

# In[106]:


!pip install python-docx

# In[ ]:




# In[107]:


from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


class CustomDocument():
  def __init__(self) -> None:
    self.content=""
    self.mathContentArray = []
    self.contentArray = []
    self.contentaction = ""
    self.doc = Document()
    

  def fullcontent(self,file_name="output.docx",font_name='Times New Roman', font_size=10):
    """_summary_ To load the full python file as docx

    Args:
        file_name (str, optional): Name of File. Defaults to "output.docx".
        font_name (str, optional): _description_. Defaults to 'Times New Roman'.
        font_size (int, optional): _description_. Defaults to 10.
    """
      # Create a new Document
      # Add each line of content to the document
    try:
      
      papra =self.doc.add_paragraph("\n".join(self.contentArray))
      if len(papra.runs) > 0:
        papra_run = papra.runs[0]
        papra_run.font.name = font_name
        papra_run.font.size = Pt(font_size) 

        # Save the document to the specified file
      self.doc.save(file_name)
      self.contentArray=[]
    except Exception as e:
      print("Exception : ",e)

  def contentmatrix(self,row,col,sumresult):
    # contentModify = "\n\nV^*_[{row}][{col}] = max({content})  = {res} \n".format(row=row+1,col=col+1,content=self.contentaction,res=sumresult)
    contentModify = "\n\nV^*_[{row}][{col}] = max({content})  = {res} \n".format(row=row+1,col=col+1,content=self.contentaction,res=sumresult)
    self.contentArray.append("----------------------------------------------------------------------------------------------")
    self.contentArray.append(contentModify)
    self.contentaction=""
    
  def addTable(self,data, heading, font_name='Times New Roman', font_size=10):
    heading_paragraph = self.doc.add_heading(level=1)
    heading_run = heading_paragraph.add_run(heading)
    heading_run.font.name = font_name
    heading_run.font.size = Pt(font_size + 2)  
    heading_run.bold = True
    
    # Add a table with the number of rows and columns based on the data
    table = self.doc.add_table(rows=len(data), cols=len(data[0]))
    table.style = 'Table Grid'  # Optional: Apply a table style
    
    # Populate the table with data and format the text
    for i, row in enumerate(data):
        for j, cell_text in enumerate(row):
            cell = table.cell(i, j)
            paragraph = cell.add_paragraph(str(cell_text))
            run = paragraph.runs[0]
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.bold = True  # Make the text bold
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
    # self.contentArray.append(table)
    
  def enwrapactions(self,action,sumValue):
    """_summary_ To Put in the document actions and 

    Args:
        action (_type_): Actions agent takes
        sumValue (_type_): The Sum value received by Bellman Equation
    """
    self.contentaction += "\n{act}<{cont} = {sumValue}>\n,".format(act=action,cont=self.content,sumValue=sumValue[action])
    self.content=""
     


# The equation is V<sub>k</sub> = max(up,down,left,right)
# <br>
# up=0,down=1,right=2,left=3
# <br>
# $$
# V^*_s = \ P(s'|a,s) \left[ R_{s,a,s'} + \gamma V^*_{s'} \right]
# $$
# 
# 

# In[108]:


GAMMA = 0.9
hellstates = [[2,1],[2,3]]
goalstate = [4,4]
Trans = {"curr":0.7,"other":0.1,"terminal":1} # Transition Functions where curr is intended state, other is the unintended state , terminal is the terminal state 

"""
# s₁,₁  s₁,₂  s₁,₃  s₁,₄
# s₂,₁  s₂,₂  s₂,₃  s₂,₄
# s₃,₁  *s₃,₂  s₃,₃  *s₃,₄
# s₄,₁  s₄,₂  s₄,₃  s₄,₄
"""
# States defined for Rewards
rewardmatrix = [
    [-0.1,-0.1,-0.1,-0.1],
    [-0.1,-0.1,-0.1,-0.1],
    [-0.1,-1.0,-0.1,-1.0],
    [-0.1,-0.1,-0.1,10]
]

# Initial state of the Answer Matrix
ansmatrix = [
    [0,0,0,0],
    [0,0,0,0],
    [0,-1,0,-1],
    [0,0,0,10]
]

QArr=[]

def action_position(row,col,action,rewardmatrix):
  """_summary_ Send the position the agent takes

  Args:
      row (_type_): Row of answer matrix
      col (_type_): Column of answer matrix
      action (_type_): Which action to take
      rewardmatrix (_type_): Matrix to  receive 

  Returns:
      _type_: _description_
  """
  p_row = row
  p_col = col
  if action == 0 and row > 0:
    p_row -= 1
    
  if action == 1 and row < len(rewardmatrix)-1:
    p_row +=1
    
  if action == 2  and col < len(rewardmatrix[0])-1:
    p_col +=1
    
  if action == 3 and col >0:
    p_col -=1
    
  return p_row,p_col

prevV = 0

actions= {"up":0,"down":1,"right":2,"left":3}
sum = {"up":0,"down":0,"right":0,"left":0}
for V in range(0,5):
  customdocument = CustomDocument()
  # Traverse row and column
  for row in range(0,len(rewardmatrix)):
    for col in range(0,len(rewardmatrix)):
      sum = {"up":0,"down":0,"right":0,"left":0}
      for idx,(key,action_value) in enumerate(actions.items()):
        for val in range(0,len(actions)):
          plus = '+' if val < len(actions)-1 else ''
          loopactionval = list(actions.values())[val]
          loop_row,loop_col = action_position(row,col,loopactionval,ansmatrix)
          #Bellman Equation used for each actions
          
          if val == action_value:
              customdocument.content += "({t1} *[{t2} + {t3}*{t4}]){p}".format(t1=Trans["curr"],t2=float(rewardmatrix[loop_row][loop_col]),t3=GAMMA,t4=float(ansmatrix[loop_row][loop_col]),p=plus)
              sum[key] += Trans["curr"]*(rewardmatrix[loop_row][loop_col] + GAMMA*ansmatrix[loop_row][loop_col])
          else:
            if [row,col] not in [hellstates,goalstate]:
              customdocument.content +="({t1} *[{t2} + {t3}*{t4}]){p}".format(t1=Trans["other"],t2=float(rewardmatrix[loop_row][loop_col]),t3=GAMMA,t4=float(ansmatrix[loop_row][loop_col]),p=plus)
            sum[key] += Trans["other"]*(rewardmatrix[loop_row][loop_col] + GAMMA*ansmatrix[loop_row][loop_col])
            
        #Check if the Agent is currently in Terminal states
        if [row,col] in [hellstates,goalstate]:
          print(f"Executed where row{row} and column{col}")
          customdocument.content +="({t1} *[{t2} + {t3}*{t4}]){p}".format(t1=Trans["terminal"],t2=float(rewardmatrix[row][col]),t3=GAMMA,t4=float(ansmatrix[row][col]))
          sum[key] = Trans["terminal"]*(rewardmatrix[row][col] + GAMMA*ansmatrix[row][col])
      
      
              
        customdocument.enwrapactions(key,sum)          
      if V == 4:
        QArr.append( list(sum.values()) )
      
      maxSum = max(sum.values())
      customdocument.contentmatrix(row,col,maxSum)
        
      
      ansmatrix[row][col]=float("{:.3f}".format(maxSum))
      # print(f"")
      
  head = "V_{no}".format(no=V+1)
  customdocument.addTable(ansmatrix,heading=head)
  customdocument.fullcontent("{head}.docx".format(head=head))

# In[109]:


import numpy as np
try:
    reshapedArr = np.array(QArr).reshape(8,8)
    Qdocument = CustomDocument()
    headQ = "Q_5"
    Qdocument.addTable(reshapedArr,heading=headQ)
    Qdocument.fullcontent("{head}.docx".format(head=headQ))
except Exception as e:
    print("Exception caused",e)

