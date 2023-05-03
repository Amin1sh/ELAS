import { makeStyles } from '@material-ui/core/styles';

export const style = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    flex: 1,
  },
  formContainer: {
    width: '100%',
    maxWidth: 'xl',
    display: 'grid',
    gridTemplateColumns: 'auto',
    gap: '48px',
    padding: '64px',
    position: 'relative',
  },
  input: {
    borderRadius: '8px',
    padding: '24px',
    '&:focus': {
      outline: 'none',
    },
  },
  select: {
    borderRadius: '8px',
    padding: '16px',
    '&:focus': {
      outline: 'none',
    },
  },
  textarea: {
    borderRadius: '8px',
    padding: '24px',
    height: '160px',
    '&:focus': {
      outline: 'none',
    },
  },
  error: {
    color: '#f44336',
  },
  submitButton: {
    backgroundColor: '#FFA500',
    '&:hover': {
      backgroundColor: '#FFB300',
    },
    borderRadius: '8px',
    padding: '32px',
    fontSize: '1rem',
    fontWeight: 'medium',
    outline: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#fff'
  },
}));