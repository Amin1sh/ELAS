import { makeStyles } from '@material-ui/core/styles';

export const style = makeStyles((theme) => ({
  flex: {
    display: 'flex',
  },
  'flex-col': {
    flexDirection: 'column',
  },
  'item-center': {
    alignItems: 'center',
  },
  'flex-1': {
    flex: 1,
  },
  'mt-8': {
    marginTop: 8,
  },
  'w-full': {
    width: '100%',
  },
  'items-stretch': {
    alignItems: 'stretch',
  },
  'bg-amber-700': {
    backgroundColor: '#ff9800',
  },
  'bg-gray-700': {
    backgroundColor: '#424242',
  },
  ulTabBox: {
    backgroundColor: '#4B5563',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: '16px',
    borderRadius: '9999px',
    padding: '8px 16px',
    listStyle: 'none',
  },
  liItemCls: {
    transition: 'color 250ms ease-in-out',
    cursor: 'pointer',
    color: 'white',
    borderRadius: '9999px',
    padding: '8px 16px',
  },
  tabBox: {
    borderRadius: '50px',
    backgroundColor: '#1a202c',
    marginTop: '12px',
    padding: '8px',
    display: 'flex',
    justifyContent: 'center',
    color: '#fff',
    flexDirection: 'column',
  },
  tabBoxLblCount: {
    fontSize: '0.875rem',
    fontWeight: 500,
    color: '#E0E0E0',
  },
  selectCount: {
    marginTop: '8px',
    display: 'block',
    width: '100%',
    paddingLeft: '24px',
    paddingRight: '80px',
    paddingTop: '8px',
    paddingBottom: '8px',
    fontSize: '1rem',
    borderWidth: '1px',
    borderColor: '#E0E0E0',
    outline: 'none',
    '&:focus': {
      outline: `2px solid #ff9800`,
      outlineOffset: '2px',
    },
    borderRadius: '10px',
    [theme.breakpoints.down('sm')]: {
      fontSize: '14px',
    },
  },
  boxChart: {
    margin: '5px 10% 8px 10%'
  },
  'mb-8': {
    marginBottom: '8px',
  },
  chartLabelCls: {
    display: 'block',
    color: '#E0E0E0',
    fontSize: '0.875rem',
    fontWeight: '500'
  },
  chartSelectCls: {
    marginTop: '4px',
    display: 'block',
    width: '100%',
    paddingLeft: '12px',
    paddingRight: '40px',
    paddingTop: '8px',
    paddingBottom: '8px',
    fontSize: '16px',
    border: '1px solid #E5E7EB',
    outline: 'none',
    '&:focus': {
      outline: '1px solid #2563EB',
      boxShadow: '0 0 0 2px rgba(37,99,235,0.25)',
    },
    '@media (max-width: 600px)': {
      fontSize: '14px',
    },
    borderRadius: '4px',
  },
  'flex-center-items': {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },

  'chart-box-3col': {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },

  'pie-chart-item-box': {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },

  'pie-chart-label': {
    fontSize: '14pt',
    fontWeight: 'bold',
    marginBottom: '20px'
  }
}));