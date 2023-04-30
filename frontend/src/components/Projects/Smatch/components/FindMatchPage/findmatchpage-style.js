import { makeStyles } from "@material-ui/core/styles";

const MatchPageStyle = makeStyles(theme => ({
    defaultStyle: {
        transform: 'rotate(0deg)',
        opacity: 1,
        transition: 'transform 500ms ease-in-out, opacity 500ms ease-in-out',
        '-webkit-transform-origin': '50% 120%',
        'transform-origin': '50% 120%',
    },
    rotate90: {
        transform: 'rotate(90deg)',
        opacity: 0
    },
    '-rotate90': {
        transform: 'rotate(-90deg)',
        opacity: 0
    },
    button: {
        WebkitAppearance: 'button',
        backgroundColor: 'transparent',
        backgroundImage: 'none',
        cursor: 'pointer',
        textTransform: 'none',
        padding: '4px',
        outline: 'none',
        border: 'none',
        '& img': {
            width: '40px',
            height: '40px',
            filter: 'invert(60%) sepia(100%) saturate(10000%) hue-rotate(57deg) brightness(2.5) contrast(1.2)'
        }
    },
    container: {
        width: '100%',
        maxWidth: 'xl',
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        padding: '20px 4px',
        overflow: 'hidden',
      },
      questionContainer: {
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        flex: 1,
        backgroundColor: 'rgb(17 24 39 / 1)',
        borderRadius: '50px',
        padding: '10px'
      },
      questionTitle: {
        color: 'rgb(245 158 11 / 1)',
        textAlign: 'center',
        fontSize: '2.25rem',
        padding: '8px',
      },
      questionContent: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '4px',
      },
      questionText: {
        color: 'rgb(255 255 255 / 1)',
        fontSize: '3rem',
        textAlign: 'center',
        '@media (min-width: 960px)': {
          fontSize: '5rem',
        },
      },
  }));
  
  export default MatchPageStyle;