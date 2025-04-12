import tkinter as tk
import matplotlib.pyplot as plt
import warnings
import numpy as np
import pandas as pd
#from scipy.stats import linregress
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

warnings.simplefilter('ignore')

def processFiles(citations_path, grant_money_path):
    citations = pd.read_csv(citations_path, encoding='ISO-8859-1')
    pd.to_numeric(citations['Citations'])
    grants = pd.read_csv(grant_money_path, encoding='ISO-8859-1', skiprows=3)
    grants['Amount($)']=pd.to_numeric(grants['Amount($)'].replace({',':''}, regex=True))
    for index in range(len(grants['Fiscal Year'])):
        grants['Fiscal Year'][index]=grants['Fiscal Year'][index][:4]
        
    grants['Fiscal Year']=pd.to_numeric(grants['Fiscal Year'])

    return citations, grants

citations, grants = processFiles('citationCount.csv', 'NSERC_Results_cs.csv')

def exit_window():
    root.destroy()



def create_text_widget():
    global text_widget 
    text_widget = tk.Text(right_frame, wrap="word")
    text_widget.pack(side="left", fill="both", expand=True)
    global scrollbar
    scrollbar = tk.Scrollbar(right_frame, orient = 'vertical', command=text_widget.yview)
    scrollbar.pack(side="right", fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    
def process_citations():
    
    
    for widget in right_frame.winfo_children():
        widget.destroy()
        
    create_text_widget()

    user_input=entry.get()
    result=0
    outputText=""
    nGrants = grants[grants['Name'].isin(citations['Name'])].set_index("Name")
    for index in range(len(citations['Name'])):
        if citations['Name'][index].__contains__(user_input):
            person=citations['Name'][index]
            result=citations['Citations'][index]
                       
            if person in nGrants.index:
                amount = nGrants.loc[person, 'Amount($)']
                nAmount = pd.Series(amount).iloc[0]
                amount_str = str(nAmount)
            else:
                amount_str = "no matching grant"
                
            outputText=outputText + f"{person} has {result} citations and received a grant of {amount_str} dollars\n       "
    if result>0:
        #output_label.config(text=f"{person} has {result} citations")
        #output_label.config(text=outputText)
        text_widget.insert(tk.END, "       " + outputText)
    else:
       text_widget.insert(tk.END, "No researcher found")
       
def plotMoneyData(citations, grants, frame):
    """
    Plots a scatter plot showing the correlation between
    citation count and grant money received, and embeds it in the Tkinter window.
    """
    
    for widget in right_frame.winfo_children():
        widget.destroy()
        
    # Get data, make citations the same length, remove grants data not found in citations
    nCitations = grants[['Name']].merge(citations[['Name', 'Citations']], on='Name', how='left')
    nCitations = nCitations.dropna()
    nGrants = grants[grants['Name'].isin(nCitations['Name'])]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(nCitations['Citations'], nGrants['Amount($)'], color='blue', alpha=0.7)
    #correlation = nGrants['Amount($)'].corr(nCitations['Citations'])
   # print(f"Correlation: {correlation:.3f}")
    
    # Labels
    ax.set_title('Correlation Between Citation Count and Grant Money Received')
    ax.set_xlabel('Number of times cited')
    ax.set_ylabel('Grant Money Received ($)')
    ax.grid(True)
    ax.ticklabel_format(style='plain', axis='y')
    
    # Trendline
    z = np.polyfit(nCitations['Citations'], nGrants['Amount($)'], 1)
    p = np.poly1d(z)
    ax.plot(nCitations['Citations'], p(nCitations['Citations']), "r--")
    
    # Embed the plot into the Tkinter window using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Ensure the plot fills the frame

if __name__=='__main__':
    root=tk.Tk()
    root.geometry("600x400")
    
    left_frame = tk.Frame(root, width=300, bg="lightgray")
    left_frame.pack(side="left", fill="both", expand=True)
    right_frame = tk.Frame(root, width=300)
    right_frame.pack(side="right", fill=tk.BOTH, expand=True)

    root.title("Enter a reseacher \"Last Name, First Name\"")
    entry=tk.Entry(left_frame, width=60)
    #entry.pack(side="top", pady=300)
    entry.place(relx=0.5,rely=0.5, anchor = 'center')
    
    text_widget=tk.Text(right_frame, wrap="word")
    text_widget.pack(side="left", fill="both", expand=True)

    citation_button=tk.Button(left_frame, text="Show Researcher", command=process_citations)
    citation_button.place(relx=0.5,rely=0.5, anchor = 'center', y=32)
    #citation_button.pack(pady=5)
    exit_button=tk.Button(left_frame, text="Exit", command=exit_window)
    exit_button.place(relx=0.5,rely=0.5, anchor = 'center', y = 96)
    #exit_button.pack(pady=5)
    scrollbar = tk.Scrollbar(right_frame, orient = 'vertical', command=text_widget.yview)
    scrollbar.pack(side="right", fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    #graph button
    graph_button = tk.Button(left_frame, text="Show Plot", command=lambda: plotMoneyData(citations, grants, right_frame))
    graph_button.place(relx=0.5,rely=0.5, anchor = 'center', y = 64)
    root.mainloop()
