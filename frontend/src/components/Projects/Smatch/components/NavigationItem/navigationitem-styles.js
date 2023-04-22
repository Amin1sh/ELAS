const styles = (theme) => ({
    root: {
      position: 'relative',
      '& img': {
        filter: 'invert(30%) grayscale(100%)'
      },
      '&.active img': {
        filter: 'invert(60%) sepia(100%) saturate(10000%) hue-rotate(57deg) brightness(2.5) contrast(1.2)'
      },
    },
    badge: {
      top: -1,
      right: -1,
      transform: 'scale(0.75)',
      backgroundColor: '#f5f5f5',
      color: '#424242',
      '& .MuiBadge-badge': {
        borderRadius: '50%',
        padding: '4px 8px',
      },
    }
  });
  
  export default styles;