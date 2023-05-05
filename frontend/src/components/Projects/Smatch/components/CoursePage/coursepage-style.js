import { makeStyles } from "@material-ui/core/styles";

const style = makeStyles((theme) => ({
  Levelcontainer: {
    display: 'flex',
    alignItems: 'flex-end',
    gap: '16px',
    height: 16,
    padding: '0px 32px',
  },
  bgActiveBar: {
    backgroundColor: '#FBBF24'
  },
  'bg-gray-400': {
    backgroundColor: '#CBD5E0'
  },
  flex: {
    display: 'flex'
  },
  'flex-1': {
    flex: '1 1 0%'
  }, 
  'h-1/3': {
    height: '33.333333%'
  },
  'h-2/3': {
    height: '66.666667%'
  },
  'h-full': {
    height: '100%'
  },
  flexCol: {
    display: 'flex',
    flexDirection: 'column',
  },
  gap4: {
    gap: '32px',
  },
  bgGray900: {
    backgroundColor: '#1F2937',
  },
  rounded30px: {
    borderRadius: '30px',
  },
  px6: {
    paddingLeft: '48px',
    paddingRight: '48px',
  },
  pb6: {
    paddingBottom: '48px',
  },
  pt4: {
    paddingTop: '32px',
  },
  textCenter: {
    textAlign: 'center',
  },
  textLg: {
    fontSize: '14pt',
  },
  textAmber500: {
    color: '#F59E0B',
  },
  textWhite: {
    color: '#fff',
  },
  textSm: {
    fontSize: '9pt',
  },
  gridContainer: {
    display: 'grid',
    gridTemplateColumns: 'auto auto',
    gap: '32px',
    padding: '32px',
    [theme.breakpoints.up('lg')]: {
      gridTemplateColumns: 'auto auto auto auto',
    },
  },
  descriptionItem: {
    gridColumn: 'span 2',
    [theme.breakpoints.up('lg')]: {
      gridColumn: 'span 4',
      gridRowStart: 2,
    },
  },
  durationItem: {
    [theme.breakpoints.up('lg')]: {
      gridColumnStart: 3,
    },
  },
  priceItem: {
    [theme.breakpoints.up('lg')]: {
      gridColumnStart: 4,
    },
  },
  courseLink: {
    backgroundColor: '#FFA500',
    color: '#fff',
    textAlign: 'center',
    borderRadius: '9999px',
    gridColumn: 'span 2',
    [theme.breakpoints.up('lg')]: {
      gridColumn: 'span 4',
    },
    padding: '8px',
    textDecoration: 'none',
  },
}));

export default style;