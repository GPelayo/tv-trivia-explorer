class EpisodeComponent extends React.Component {
    render() {
        return <div><h3> { this.props.episode['title'] }</h3>
            <ul>
                { this.props.episode['trivia'].map( function(t) { return <li>{ t['fact'] }</li> } ) }
            </ul>
            </div>
    }
}

class SeasonComponent extends React.Component {
    render() {
        return  <div>
                <h2>Season { this.props.season['number'] }</h2>
                { this.props.season['episodes'].map( function(e) { return <EpisodeComponent episode={ e['episode'] }/> } ) }
                </div>
    }
}
var TVTriviaSearch = React.createClass({
  getInitialState: function(){
    return {
    titleInput: '',
    seasonInput: '',
    showData: ''};
  },
  handleSubmit: function(event){
    var searchClass = this;
    var query_string =  "title=" + this.state.titleInput +
                        (this.state.seasonInput ? ("&season=" + this.state.seasonInput) : "") +
                        (this.state.yearInput ? ("&year=" + this.state.yearInput) : "");
    $.ajax({
        url: "/show?" + query_string,
        dataType: 'json',
        beforeSend: function (){
            $('.status').text('Loading...');
        },
        complete: function() {
            $('.status').text('');
        },
        success: function(data) {
            searchClass.setState({ showData:data });
        }
    });
    event.preventDefault();
  },
  handleTitleChange: function(event){
    this.setState({ titleInput: event.target.value })
  },
  handleYearChange: function(event){
    this.setState({ yearInput: event.target.value })
  },
  handleSeasonChange: function(event){
    this.setState({ seasonInput: event.target.value })
  },
  render: function() {
    var season_list_data = [];
    var showData =  this.state.showData['show']
    var title = "";

    if(showData) {
        season_list_data = showData['seasons'];
        title = showData['title'] + " (" + showData['year_start'] + "-" + showData['year_end'] + ")";
    }
    return (
        <div>
            <form onSubmit={this.handleSubmit}>
                <div className="form_container">
                    <div className="start_at_container">
                        <div className="form_input">
                            <label for='title'>Title: </label><br/>
                            <input idName="title" type="text"value={this.state.titleInput} onChange={this.handleTitleChange}/>
                        </div>
                        <div className="form_input">
                            <label for='year'>Year: </label><br/>
                            <input idName="year" className="small_input" type="number" label="Year" value={this.state.yearInput} onChange={this.handleYearChange}/><br/>
                        </div>
                        <div className="form_input">
                            <label for='season'>Season: </label><br/>
                            <input idName="season" className="small_input" type="text" label="Season" placeholder="1" value={this.state.seasonInput} onChange={this.handleSeasonChange}/>
                        </div>
                        <div className="form_input">
                            <div className="status"></div>
                        </div>
                    </div><br/>
                    <div className="form_input">
                        <input type="submit" value="Search"/><br/>
                    </div>
                </div>
            </form>
           <div className="trivia_container">
                <h1> { title } </h1>
                { season_list_data.map(function(s) { return <SeasonComponent season= { s['season'] }/> }) }
           </div>
        </div>
    )
  }

});

ReactDOM.render(
  <TVTriviaSearch/>,
  document.getElementById('content')
);
