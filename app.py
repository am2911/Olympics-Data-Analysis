import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('olympic-bright-circle-colorful-wallpaper-preview.jpg')
user_menu=st.sidebar.radio(
    " Selct an Options",
    ("Medal Tally","Overall Analysis","Country-wise-Analysis","Athlete-wise-Analysis")
)

if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year(df)
    
    selected_year=st.sidebar.selectbox("select Year",years)
    selected_country=st.sidebar.selectbox("select country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    
    if selected_year=="Overall" and selected_country=="Overall":
        st.title('Overall Tally')
    
    if selected_year!="Overall" and selected_country=="Overall":
        st.title('Medal Tally in '+ str(selected_year) + " Olympics")
    
    if selected_year=="Overall" and selected_country!="Overall":
        st.title(selected_country + " Overall Performance")
    
    if selected_year!="Overall" and selected_country!="Overall":
        st.title(selected_country + " Performace in " + str(selected_year))

    st.table(medal_tally)

# Overall Analysis
if user_menu=="Overall Analysis":
    editions=df["Year"].unique().shape[0]-1
    city=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    natioins=df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(city)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(natioins)

    nations_over_time=helper.data_over_time(df,"region")
    nations_over_time.rename(columns={"index":"Edition","region":"No of Countries"},inplace=True)
    fig=px.line(nations_over_time,x="Edition",y="No of Countries")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    
    events_over_time=helper.data_over_time(df,"Event")
    events_over_time.rename(columns={"index":"Edition","Event":"No of Events"},inplace=True)
    fig=px.line(events_over_time,x="Edition",y="No of Events")
    st.title("Events over the years")
    st.plotly_chart(fig)
    
    athletes_over_time=helper.data_over_time(df,"Name")
    athletes_over_time.rename(columns={"index":"Edition","Name":"No of Athletes"},inplace=True)
    fig=px.line(athletes_over_time,x="Edition",y="No of Athletes")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of Events over time (Every Sports)")
    fig ,ax=plt.subplots(figsize=(20,20))    
    x=df.drop_duplicates(subset=["Year","Sport","Event"])
    sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)

    # Most Successful Athlete
    st.title("Most Successful Athlete")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")

    selected_sport=st.selectbox("select a Sport",sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu==("Country-wise-Analysis"):
    st.sidebar.title("Country-wise-Analysis")
    country_list=df["region"].dropna().unique().tolist()
    country_list.sort()
    #country_list.insert(0,"Overall")
    selected_country=st.sidebar.selectbox("select a Country",country_list)

    country_df=helper.YearWise_medal_tally(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country+" excels in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig ,ax=plt.subplots(figsize=(20,20))  
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of "+selected_country)
    top10_df=helper.TopAthletes(df,selected_country)
    st.table(top10_df)

# Athlete- wise-analysis
if user_menu==("Athlete-wise-Analysis"):
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    
    x1=athlete_df["Age"].dropna()
    x2=athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3=athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    x4=athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    
    fig=ff.create_distplot([x1,x2,x3,x4],["Overall Age","Gold Medalist","Silver Medalist","Bronze Medalist"],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.markdown("<h2 style='text-align: center; color: white;'>Distribution of Age</h2>", unsafe_allow_html=True)

    st.plotly_chart(fig)

    # Distribution of Age
    x=[]
    names=[]
    famous_sport=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
        'Ice Hockey']

    for sport in famous_sport:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df["Medal"]=="Gold"]["Age"].dropna())
        names.append(sport)

    fig=ff.create_distplot(x,names,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.markdown("<h2 style='text-align: center; color: white;'> Distribution of Age wrt Sports (Gold Medalist)</h2>", unsafe_allow_html=True)

    st.plotly_chart(fig)

    # Height vs Weight Graph
    st.markdown("<h2 style='text-align: center; color: white;'> Weight Vs Height</h2>", unsafe_allow_html=True)
    
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")

    selected_sport=st.selectbox("select a Sport",sport_list)
    temp_df=helper.weightVsHeight(df,selected_sport)
    fig,ax=plt.subplots()

    ax=sns.scatterplot(temp_df["Weight"],temp_df["Height"],hue=temp_df["Medal"],style=temp_df["Sex"],s=30)
    st.pyplot(fig)

    # men vs woemn participation
    st.markdown("<h2 style='text-align: center; color: white;'> Men Vs Women Participation Over the Years </h2>", unsafe_allow_html=True)
    final=helper.menVsWomen(df)
    fig=px.line(final,x="Year",y=['Male','Female'])
    fig.update_layout(autosize=False,width=800,height=600)
    st.plotly_chart(fig)